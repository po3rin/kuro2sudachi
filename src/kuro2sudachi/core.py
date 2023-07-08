import argparse
import fileinput
import json
import os
import re
from dataclasses import dataclass

import jaconv
from sudachipy import dictionary, tokenizer

from kuro2sudachi.normalizer import SudachiCharNormalizer

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
    help="remove words system dict already exist",
)
parser.add_argument("-r", "--sudachi_setting", help="the setting file in JSON format")
parser.add_argument("-s", "--sudachi_dict_type", help="sudachidict type")
parser.add_argument(
    "-u",
    "--unit_word_dict",
    default="",
    help="A dictionary for split registration of words that are not in the system dictionary. Must be specified as a user dictionary in sudachi's configuration file (json).",
)
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


@dataclass
class UnitWord:
    word_id: int
    line: str


class Converter:
    def __init__(
        self,
        rewrite_file,
        config=None,
        sudachi_setting=None,
        dict_type="core",
        rm=False,
        unit_words_dict: dict[str, UnitWord] = {},
    ):
        if rewrite_file == "":
            raise DictFormatError("rewrite.def file path is required")

        self.tokenizer = dictionary.Dictionary(
            config_path=sudachi_setting, dict=dict_type
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
        self.unit_words_dict = unit_words_dict

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

    def split_info(self, normalized: str, udm: list[str], mode: any) -> str:
        word_ids = []
        oov = []
        for m in self.tokenizer.tokenize(normalized, mode):
            if ",".join(m.part_of_speech()) == "名詞,数詞,*,*,*,*":
                return "*"

            if m.is_oov() or m.dictionary_id() == -1:
                oov.append(m.surface())
                continue

            if str(m) in self.unit_words_dict:
                word_ids.append(f"U{str(self.unit_words_dict[str(m)].word_id)}")
            else:
                word_ids.append(str(m.word_id()))

        if len(oov) > 0:
            raise OOVError(f"split word has out of vocab: {oov} in {normalized}")

        return "/".join(word_ids)

    def split(self, normalized: str, udm: list[str]) -> str:
        try:
            unit_div_info = []
            if "A" in udm:
                info = self.split_info(normalized, udm, tokenizer.Tokenizer.SplitMode.A)
                unit_div_info.append(info)
            else:
                unit_div_info.append("*")

            if "B" in udm:
                info = self.split_info(normalized, udm, tokenizer.Tokenizer.SplitMode.B)
                unit_div_info.append(info)
            else:
                unit_div_info.append("*")

            return ",".join(unit_div_info)
        except OOVError as e:
            raise e


def cli() -> str:
    args = parser.parse_args()
    out = open(args.out, "wt")
    rewrite = args.rewrite_def
    rm = args.rm_already_exist
    config = args.config
    sudachi_setting = args.sudachi_setting
    sudachi_dict_type = args.sudachi_dict_type
    unit_word_dict = args.unit_word_dict

    unit_words_dict: dict[str, UnitWord] = {}
    if not unit_word_dict == "":
        with fileinput.input(files=unit_word_dict) as merge_dict:
            for i, line in enumerate(merge_dict):
                line = line.replace("\n", "")
                unit_words_dict[line.split(",")[0]] = UnitWord(word_id=i, line=line)
                out.write(f"{line}\n")

    c = Converter(
        rewrite,
        config,
        sudachi_setting=sudachi_setting,
        dict_type=sudachi_dict_type,
        rm=rm,
        unit_words_dict=unit_words_dict,
    )

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
