from kuro2sudachi.core import convert
import fileinput


def test_kuro2sudachi_cli(capsys):
    sudachi_dict_lines = []
    with fileinput.input(files="tests/sudachi_dict_test.txt") as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            sudachi_dict_lines.append(line)

    with fileinput.input(files="tests/kuromoji_dict_test.txt") as input:
        for i, line in enumerate(input):
            line = line.strip()
            if line == "":
                continue

            result = convert(line)
            assert result == sudachi_dict_lines[i]
