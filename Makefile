PYTHONPATH=.
export PYTHONPATH
test:
	pytest -s --cov=notify_sms_py --cov-fail-under=50 --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml tests/

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
	autoflake -r --in-place --remove-unused-variables notify_sms_py tests

format: clean
	black --check .

lint:
	pylint notify_sms_py tests --rcfile=.pylintrc

all: clean test format

build:
	rm -rf dist
	python3 -m build

publish: build
	python3 -m twine upload dist/*
	