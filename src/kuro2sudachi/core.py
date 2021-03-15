import re
import json
import argparse
import fileinput
import jaconv

from kuro2sudachi.normalizer import SudachiCharNormalizer


parser = argparse.ArgumentParser(
    description="convert kuromoji user dict to sudacchi user dict"
)
parser.add_argument("file", help="kuromoji dict file path")
parser.add_argument(
    "-s",
    "--setting",
    help="convert setting file (json format file)",
)
parser.add_argument("-o", "--out", help="output path")
parser.add_argument(
    "-r", "--rewrite", help="rewrite text file path (default: ./rewrite.def)"
)
parser.add_argument(
    "--ignore",
    action="store_true",
    help="ignore invalid format line or unsupported pos error",
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


class Converter:
    def __init__(self, rewrite_file="rewrite.def", setting=None):
        if setting is not None:
            with open(setting) as f:
                s = json.load(f)
        else:
            s = default_setting

        self.rewrite = rewrite_file
        self.setting = s

    def convert(self, line: str) -> str:
        data = line.split(",")
        try:
            word = data[0]
            # splited = data[1]
            yomi = self.nomlized_yomi(data[2])
            pos = self.pos_convert(data[3])
        except IndexError:
            raise DictFormatError(f"'{line}' is invalid format")

        normalizer = SudachiCharNormalizer(rewrite_def_path=self.rewrite)
        normalized = normalizer.rewrite(word)
        return f"{normalized},{pos['left_id']},{pos['right_id']},{pos['cost']},{word},{pos['sudachi_pos']},{yomi},{word},*,*,*,*,*"

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
        else:
            return ""
        return ""


def cli() -> str:
    args = parser.parse_args()
    out = open(args.out, "wt")
    rewrite = args.rewrite
    setting = args.setting

    c = Converter(rewrite, setting)

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
            except (UnSupportedPosError, DictFormatError) as e:
                if args.ignore:
                    continue
                else:
                    raise e

            out.write(f"{converted}\n")
