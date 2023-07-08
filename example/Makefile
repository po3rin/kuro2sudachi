dic:
	sudachi ubuild config/sudachi_unit_word.txt -s config/system_core.dic -o config/sudachi_unit_word.dic
	poetry run kuro2sudachi config/kuromoji_dict.txt -c config/kuro2sudachi.json -r config/sudachi_for_build.json -u config/sudachi_unit_word.txt --ignore -o config/sudachi_user_dict.txt 
	sudachi ubuild config/sudachi_user_dict.txt -s config/system_core.dic -o config/sudachi_user.dic 