# example

generate sudachi user dict form kuromoji dict.

```sh
$ poetry run kuro2sudachi config/kuromoji_dict.txt -s full -o config/sudachi_user_dict.txt -c config/convert_config.json --ignore
$ poetry run sudachipy ubuild config/sudachi_user_dict.txt -o config/sudachi_user.dic
```

check

```sh
$ echo "融合たんぱく質" | sudachipy -m C -s full -r config/sudachi.json
融合たんぱく質  名詞,普通名詞,一般,*,*,*        融合たんぱく質

$ echo "融合たんぱく質" | sudachipy -m B -s full -r config/sudachi.json
融合    名詞,普通名詞,サ変可能,*,*,*    融合
たんぱく質      名詞,普通名詞,一般,*,*,*        蛋白質
```
