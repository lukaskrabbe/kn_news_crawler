pip/install:
	pip-compile requirements.in
	pip install -r requirements.txt

py/lint:
	pylint ./src

py/test:
	python -m pytest
