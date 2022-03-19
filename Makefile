lint:
	pre-commit run --all-files

test:
	coverage run -m pytest -v

coverage: test
	coverage report -m
	coverage report -m > coverage_report.log
	coverage html
	open htmlcov/index.html

install:
	pip install -r requirements.txt
	pre-commit install
