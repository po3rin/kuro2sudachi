# kuro2sudachi

[![PyPi version](https://img.shields.io/pypi/v/kuro2sudachi.svg)](https://pypi.python.org/pypi/kuro2sudachi/)
![PyTest](https://github.com/po3rin/kuro2sudachi/workflows/PyTest/badge.svg)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-390/)

kuro2sudachi lets you to convert kuromoji user dict to sudachi user dict.

## Usage

```sh
$ pip install kuro2sudachi
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
$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt -c kuro2sudachi.json
```

if you want to ignore unsupported pos error & invalid format, use `--ignore` flag.

## Dictionary type

You can specify the dictionary with the tokenize option -s (default: core).

```sh
$ pip install sudachidict_full
$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt -s full
```

## Auto Splitting

kuro2sudachi supports suto splitting.

```json
{
    "名詞": {
        "sudachi_pos": "名詞,普通名詞,一般,*,*,*",
        "left_id": 5146,
        "right_id": 5146,
        "cost": 5000,
        "split_mode": "C",
        "unit_div_mode": [
            "A", "B"
        ]
    }
}
```

output includes unit devision info.

```sh
$ cat kuromoji_dict.txt
融合たんぱく質,融合たんぱく質,融合たんぱく質,名詞
発作性心房細動,発作性心房細動,発作性心房細動,名詞

$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt -c kuro2sudachi.json --ignore

$ cat sudachi_user_dict.txt
融合たんぱく質,4786,4786,5000,融合たんぱく質,名詞,普通名詞,一般,*,*,*,,融合たんぱく質,*,C,*,660881/810248,*
発作性心房細動,4786,4786,5000,発作性心房細動,名詞,普通名詞,一般,*,*,*,,発作性心房細動,*,C,584006/434835/428494/619020,2756385/428494/619020,*
```

## Splitting Words defined by kuromoji

Currently, the CLI does not support word splitting defined by kuromoji. Therefore, the split representation of kuromoji is ignored.

```
中咽頭ガン,中咽頭 ガン,チュウイントウ ガン,カスタム名詞
↓
中咽頭ガン,4786,4786,7000,中咽頭ガン,名詞,固有名詞,一般,*,*,*,チュウイントウガン,中咽頭ガン,*,*,*,*,*
```

# For Developer

test kuro2sudachi

```sh
$ poetry install
$ poetry run pytest
```

exec kuro2sudachi command

```sh
$ poetry run kuro2sudachi tests/kuromoji_dict_test.txt -o sudachi_user_dict.txt
```
