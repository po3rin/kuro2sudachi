# kuro2sudachi

kuro2sudachi lets you to convert kuromoji user dict to sudachi user dict.

# develop

test kuro2sudachi

```sh
$ poetry install
$ poetry run pytest
```

exec kuro2sudachi command

```sh
$ poetry run kuro2sudachi tests/kuromoji_dict_test.txt -o sudachi_user_dict.txt
```

## supported pos

* 固有名詞 -> 名詞,固有名詞,一般,*,*,*
* 名刺 -> 名詞,普通名詞,一般,*,*,*

