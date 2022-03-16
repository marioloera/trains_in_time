lint:
	pre-commit run --all-files

test:
	coverage run -m pytest

coverage: test
	coverage report -m

install:
	pip install -r requirements.txt
	pre-commit install
