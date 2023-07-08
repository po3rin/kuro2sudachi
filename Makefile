build:
	poetry build

format:
	poetry run black src/kuro2sudachi/*.py

publish:
	poetry run twine upload dist/*
