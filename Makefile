lint:
	pre-commit run --all-files

test:
	pytest -v

test-server:
	pytest src/server_tests -v

test-local:
	pytest src/tests -v

coverage:
	coverage run -m pytest -v
	coverage report -m
	coverage report -m > coverage_report.txt
	coverage html
	open htmlcov/index.html

install:
	pip install -r requirements.txt
	pre-commit install
