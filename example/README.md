# example

generate sudachi user dict form kuromoji dict.

```sh
## in example directory

$ curl -O -L http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict/sudachi-dictionary-20230110-core.zip && \
    unzip sudachi-dictionary-20230110-core.zip && \
    cp sudachi-dictionary-20230110/system_core.dic ./config/system_core.dic

## prepare dict for merge to avoid oov
$ sudachi ubuild config/sudachi_user_dict_for_merge.txt -o config/sudachi_user_for_merge.dic -s config/system_core.dic

## convert
$ poetry run kuro2sudachi config/kuromoji_dict.txt -o config/sudachi_user_dict.txt -c config/convert_config.json --ignore -r config/sudachi_for_build.json -m config/sudachi_user_dict_for_merge.txt

## build
$ sudachi ubuild config/sudachi_user_dict.txt -o config/sudachi_user.dic -s config/system_core.dic
```

```
$ echo '三尖弁閉鎖不全症兼肺動脈弁狭窄症' | sudachipy -r config/sudachi.json -m A
三尖弁  名詞,普通名詞,一般,*,*,*        三尖弁
閉鎖    名詞,普通名詞,サ変可能,*,*,*    閉鎖
不全    名詞,普通名詞,一般,*,*,*        不全
症      接尾辞,名詞的,一般,*,*,*        症
兼      名詞,普通名詞,一般,*,*,*        兼
肺      名詞,普通名詞,一般,*,*,*        肺
動脈    名詞,普通名詞,一般,*,*,*        動脈
弁      名詞,普通名詞,一般,*,*,*        弁
狭窄    名詞,普通名詞,形状詞可能,*,*,*  狭窄
症      接尾辞,名詞的,一般,*,*,*        症
EOS

$ echo '三尖弁閉鎖不全症兼肺動脈弁狭窄症' | sudachipy -r config/sudachi.json -m B
三尖弁  名詞,普通名詞,一般,*,*,*        三尖弁
閉鎖    名詞,普通名詞,サ変可能,*,*,*    閉鎖
不全    名詞,普通名詞,一般,*,*,*        不全
症      接尾辞,名詞的,一般,*,*,*        症
兼      名詞,普通名詞,一般,*,*,*        兼
肺動脈  名詞,普通名詞,一般,*,*,*        肺動脈
弁      名詞,普通名詞,一般,*,*,*        弁
狭窄    名詞,普通名詞,形状詞可能,*,*,*  狭窄
症      接尾辞,名詞的,一般,*,*,*        症
EOS

$ echo '三尖弁閉鎖不全症兼肺動脈弁狭窄症' | sudachipy -r config/sudachi.json -m C
三尖弁閉鎖不全症兼肺動脈弁狭窄症        名詞,普通名詞,一般,*,*,*        三尖弁閉鎖不全症兼肺動脈弁狭窄症
EOS
```
