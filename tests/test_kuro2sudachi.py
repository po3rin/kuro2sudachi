from kuro2sudachi.core import Converter
import fileinput


def test_kuro2sudachi_cli(capsys):
    sudachi_dict_lines = []
    c = Converter(dict_type="full", rm=True)

    with fileinput.input(files="tests/sudachi_dict_test.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)

    print(sudachi_dict_lines)

    with fileinput.input(files="tests/kuromoji_dict_test.txt") as input:
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
            assert result == sudachi_dict_lines[count]
            count += 1


def test_kuro2sudachi_with_custom_pos_cli(capsys):
    c = Converter(dict_type="full",
                  config="tests/convert_config.json", rm=True)

    sudachi_dict_lines = []
    with fileinput.input(files="tests/sudachi_with_custom_pos_dict.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            sudachi_dict_lines.append(line)
    print(sudachi_dict_lines)

    with fileinput.input(files="tests/kuromoji_dict_test.txt") as input:
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
            assert result == sudachi_dict_lines[count]
            count += 1
