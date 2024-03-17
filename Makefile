test:
	pytest -s --cov=notify --cov-fail-under=50 --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml tests/

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
	autoflake -r --in-place --remove-unused-variables notify tests

format: clean
	pylint notify tests --rcfile=.pylintrc
	black --check .