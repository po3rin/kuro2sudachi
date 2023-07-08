import fileinput

from kuro2sudachi.core import Converter, OOVError


def test_kuro2sudachi_cli(capsys):
    sudachi_dict_lines = []
    c = Converter(rewrite_file="./tests/rewrite.def", dict_type="full", rm=True)

    with fileinput.input(files="tests/sudachi_dict.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict.txt") as input:
        count = 0
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            result = c.convert(line)
            if result == "":
                continue

            print(result)
            print(sudachi_dict_lines[count])
            assert result == sudachi_dict_lines[count]
            count += 1


def test_kuro2sudachi_with_custom_pos_cli(capsys):
    c = Converter(
        rewrite_file="./tests/rewrite.def",
        dict_type="full",
        config="tests/convert_config.json",
        rm=True,
    )

    sudachi_dict_lines = []
    with fileinput.input(files="tests/sudachi_dict_with_custom_pos.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict.txt") as input:
        count = 0
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            result = c.convert(line)
            if result == "":
                continue
            assert result == sudachi_dict_lines[count]
            count += 1

def test_kuro2sudachi_with_split(capsys):
    c = Converter(
        rewrite_file="./tests/rewrite.def",
        dict_type="full",
        config="tests/convert_config.json",
        rm=True,
        
    )

    sudachi_dict_lines = []
    with fileinput.input(files="tests/sudachi_dict_with_split_mode.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict_with_split_mode.txt") as input:
        count = 0
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            try:
                result = c.convert(line)
                if result == "":
                    continue
            except OOVError: 
                continue

            assert result == sudachi_dict_lines[count]
            count += 1
