from kuro2sudachi.core import Converter
import fileinput


def test_kuro2sudachi_cli(capsys):
    sudachi_dict_lines = []
    c = Converter()

    with fileinput.input(files="tests/sudachi_dict_test.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict_test.txt") as input:
        for i, line in enumerate(input):
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            result = c.convert(line)
            assert result == sudachi_dict_lines[i]


def test_kuro2sudachi_with_custom_pos_cli(capsys):
    c = Converter(setting="tests/convert_setting.json")

    sudachi_dict_lines = []
    with fileinput.input(files="tests/sudachi_with_custom_pos_dict.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict_test.txt") as input:
        for i, line in enumerate(input):
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue

            result = c.convert(line)
            assert result == sudachi_dict_lines[i]
