PYTHONPATH=.
export PYTHONPATH
APP_NAME=notify_sms_py
WORKDIRS=${APP_NAME} tests
test:
	pytest -s --cov=${APP_NAME} --cov-fail-under=50 --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml tests/

clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .coverage.*
	rm -rf htmlcov
	rm -rf .tox
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports ${WORKDIRS}

format: clean
	black .
	black --check .

lint:
	pylint ${WORKDIRS} --rcfile=.pylintrc

all: lint format

build:
	rm -rf dist
	python3 -m build

publish: build
	python3 -m twine upload dist/*
	