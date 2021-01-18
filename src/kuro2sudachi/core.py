import re
import argparse
import fileinput
import jaconv
import sys

from kuro2sudachi.normalizer import SudachiCharNormalizer


parser = argparse.ArgumentParser(
    description='convert kuromoji user dict to sudacchi user dict')
parser.add_argument('file', help='kuromoji dict file path')
parser.add_argument('-o', '--out', help='output path')

pos_dict = {"固有名詞": "名詞,固有名詞,一般,*,*,*", "名詞": "名詞,普通名詞,一般,*,*,*"}

p = re.compile('[\u30A1-\u30FC]*')


def nomlized_yomi(yomi: str) -> str:
    yomi = jaconv.hira2kata(yomi)
    if p.fullmatch(yomi):
        return yomi
    else:
        return ""
    return ""


def pos_convert(pos: str) -> str:
    try:
        spos = pos_dict[pos]
        return spos
    except KeyError:
        print(f"{pos} is not supported pos")
        sys.exit(1)


def convert(line: str) -> str:
    data = line.split(',')
    word = data[0]
    # splited = data[1]
    yomi = nomlized_yomi(data[2])
    pos = pos_convert(data[3])

    normalizer = SudachiCharNormalizer()
    normalized = normalizer.rewrite(word)
    return f'{normalized},4786,4786,5000,{word},{pos},{yomi},{word},*,*,*,*,*'


def cli() -> str:
    args = parser.parse_args()
    out = open(args.out, "wt")
    with fileinput.input(files=args.file) as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            converted = convert(line)
            out.write(f'{converted}\n')
