# kuro2sudachi

[![PyPi version](https://img.shields.io/pypi/v/kuro2sudachi.svg)](https://pypi.python.org/pypi/kuro2sudachi/)
![PyTest](https://github.com/po3rin/kuro2sudachi/workflows/PyTest/badge.svg)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-390/)

kuro2sudachi lets you to convert kuromoji user dict to sudachi user dict.

## Usage

```sh
$ pip install kuro2sudachi

# prepase riwirte.def
# https://github.com/WorksApplications/Sudachi/blob/develop/src/main/resources/rewrite.def
$ ls
rewiite.def

$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt
```

## Custom pos convert dict

you can overwrite convert config with setting json file.

```json
{
    "固有名詞": {
        "sudachi_pos": "名詞,固有名詞,一般,*,*,*",
        "left_id": 4786,
        "right_id": 4786,
        "cost": 5000
    },
    "名詞": {
        "sudachi_pos": "名詞,普通名詞,一般,*,*,*",
        "left_id": 5146,
        "right_id": 5146,
        "cost": 5000
    }
}

```

```$
$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt -c convert_config.json
```

if you want to ignore unsupported pos error & invalid format, use `--ignore` flag.

## Dictionary type

You can specify the dictionary with the tokenize option -s (default: core).

```sh
$ pip install sudachidict_full
$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt -s full
```

## Splitting Words

Currently, the CLI does not support word splitting. Therefore, the split representation of kuromoji is ignored.

```
中咽頭ガン,中咽頭 ガン,チュウイントウ ガン,カスタム名詞
↓
中咽頭ガン,4786,4786,7000,中咽頭ガン,名詞,固有名詞,一般,*,*,*,チュウイントウガン,中咽頭ガン,*,*,*,*,*
```

# Develop

test kuro2sudachi

```sh
$ poetry install
$ poetry run pytest
```

exec kuro2sudachi command

```sh
$ poetry run kuro2sudachi tests/kuromoji_dict_test.txt -o sudachi_user_dict.txt
```

## TODO

- [ ] split mode
- [ ] default rewrite
