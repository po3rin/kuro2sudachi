# example

generate sudachi user dict form kuromoji dict.

```sh
## prepare dict for merge to avoid oov
$ sudachipy ubuild config/sudachi_user_dict_for_merge.txt -o config/sudachi_user_for_merge.dic

## convert
$ poetry run kuro2sudachi config/kuromoji_dict.txt -o config/sudachi_user_dict.txt -c config/convert_config.json --ignore -r config/sudachi.json -m config/sudachi_user_dict_for_merge.txt

## build
$ sudachipy ubuild config/sudachi_user_dict.txt -o config/sudachi_user.dic
```
