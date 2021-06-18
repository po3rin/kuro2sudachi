from sudachipy import dictionary
from sudachipy import tokenizer
from sudachipy.plugin import oov
from kuro2sudachi.normalizer import SudachiCharNormalizer
import jaconv
import fileinput
import argparse
import json
import os
import re


mode = tokenizer.Tokenizer.SplitMode.C

parser = argparse.ArgumentParser(
    description="convert kuromoji user dict to sudacchi user dict"
)
parser.add_argument("file", help="kuromoji dict file path")
parser.add_argument(
    "-c",
    "--config",
    help="convert config file (json format file)",
)
parser.add_argument("-o", "--out", help="output path")
parser.add_argument(
    "-d",
    "--rewrite_def",
    default=os.path.dirname(os.path.abspath(__file__)) + "/rewrite.def",
    help="rewrite text file path",
)
parser.add_argument(
    "--rm_already_exist",
    action="store_true",
    help="remove words system dict already exist"
)
parser.add_argument("-r", "--sudachi_setting", help="the setting file in JSON format")
parser.add_argument("-s", "--sudachi_dict_type", help="sudachidict type")
parser.add_argument("-m", "--merge_dict", help="A dictionary for split registration of words that are not in the system dictionary. Must be specified as a user dictionary in sudachi's configuration file (json).")
parser.add_argument(
    "--ignore",
    action="store_true",
    help="ignore invalid format line / unsupported pos error / oov error in splitted word",
)

default_setting = {
    "固有名詞": {
        "sudachi_pos": "名詞,固有名詞,一般,*,*,*",
        "left_id": 4786,
        "right_id": 4786,
        "cost": 7000,
    },
    "名詞": {
        "sudachi_pos": "名詞,普通名詞,一般,*,*,*",
        "left_id": 5146,
        "right_id": 5146,
        "cost": 7000,
    },
}

p = re.compile("[\u30A1-\u30FC]*")


class Error(Exception):
    pass


class UnSupportedPosError(Error):
    pass


class DictFormatError(Error):
    pass


class OOVError(Error):
    pass


class Converter:
    def __init__(
        self,
        rewrite_file,
        config=None,
        sudachi_setting=None,
        dict_type="core",
        rm=False,
    ):
        if rewrite_file == "":
            raise DictFormatError(f"rewrite.def file path is required")

        self.tokenizer = dictionary.Dictionary(
            dict_type=dict_type, config_path=sudachi_setting
        ).create()

        if config is not None:
            with open(config) as f:
                s = json.load(f)
        else:
            s = default_setting

        self.rewrite = rewrite_file
        self.setting = s
        self.rm = rm
        self.normalizer = SudachiCharNormalizer(rewrite_def_path=self.rewrite)

    def convert(self, line: str) -> str:
        data = line.split(",")
        try:
            word = data[0]
            # splited = data[1]
            yomi = self.nomlized_yomi(data[2].replace(" ", ""))
            pos = self.pos_convert(data[3].replace(" ", ""))
        except IndexError:
            raise DictFormatError(f"'{line}' is invalid format")

        words = [m.surface() for m in self.tokenizer.tokenize(word, mode)]

        # alrady exists in system dic
        if self.rm and len(words) == 1:
            return ""

        normalized = self.normalizer.rewrite(word)
        unit_div_info = "*,*"

        try:
            if (udm := pos.get("unit_div_mode")) != None:
                unit_div_info = self.split(normalized, udm)
        except OOVError as e:
            print(e)
            raise e

        split_mode = pos.get("split_mode", "*")
        return f"{normalized},{pos['left_id']},{pos['right_id']},{pos['cost']},{word},{pos['sudachi_pos']},{yomi},{word},*,{split_mode},{unit_div_info},*"

    def pos_convert(self, pos: str):
        try:
            spos = self.setting[pos]
            return spos
        except KeyError:
            raise UnSupportedPosError(f"{pos} is not supported pos")

    def nomlized_yomi(self, yomi: str) -> str:
        yomi = jaconv.hira2kata(yomi)
        if p.fullmatch(yomi):
            return yomi
        return ""

    def split(self, normalized: str, udm: list[str]) -> str:
        unit_div_info = []
        if "A" in udm:
            words = []
            oov = []
            for m in self.tokenizer.tokenize(normalized, tokenizer.Tokenizer.SplitMode.A):
                if m.is_oov():
                    oov.append(m.surface())
                    continue
                # if m.dictionary_id():
                #     info = f'U{m.word_id()}'

                info = f'{m.surface()},{",".join(m.part_of_speech())},{m.reading_form()}'

                words.append(info)

            if len(oov) > 0:
                raise OOVError(f"split word has out of vocab: {oov} in {normalized}")

            info = "/".join(words)
            unit_div_info.append(f'"{info}"')
        else:
            unit_div_info.append("*")

        if "B" in udm:
            words = []
            oov = []
            for m in self.tokenizer.tokenize(normalized, tokenizer.Tokenizer.SplitMode.B):
                if m.is_oov():
                    oov.append(m.surface())
                    continue
                info = f'{m.surface()},{",".join(m.part_of_speech())},{m.reading_form()}'
                words.append(info)

            if len(oov) > 0:
                raise OOVError(f"split word has out of vocab: {oov} in {normalized}")

            info = "/".join(words)
            unit_div_info.append(f'"{info}"')
        else:
            unit_div_info.append("*")

        return ",".join(unit_div_info)


def cli() -> str:
    args = parser.parse_args()
    out = open(args.out, "wt")
    rewrite = args.rewrite_def
    rm = args.rm_already_exist
    config = args.config
    sudachi_setting = args.sudachi_setting
    sudachi_dict_type = args.sudachi_dict_type
    merge_dict = args.merge_dict

    c = Converter(
        rewrite,
        config,
        sudachi_setting=sudachi_setting,
        dict_type=sudachi_dict_type,
        rm=rm,
    )

    with fileinput.input(files=merge_dict) as merged:
        for line in merged:
            line = line.replace("\n" , "")
            out.write(f"{line}\n")

    with fileinput.input(files=args.file) as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            converted = ""
            try:
                converted = c.convert(line)
                if converted == "":
                    continue
            except (UnSupportedPosError, DictFormatError, OOVError) as e:
                if args.ignore:
                    continue
                else:
                    raise e
            out.write(f"{converted}\n")
