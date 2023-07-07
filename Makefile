build:
	poetry build

format:
	poetry run black src/kuro2sudachi/*.py

publish:
	twine upload dist/*
