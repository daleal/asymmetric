POETRY = $(shell which poetry)
POETRY_VERSION = 1.1.2

# Env stuff
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

venv-with-dependencies:
	python3 -m venv .venv
	$(POETRY) run pip install --upgrade pip
	$(POETRY) run poetry install

# Passive linters
black:
	$(POETRY) run black asymmetric --check

flake8:
	$(POETRY) run flake8 asymmetric

isort:
	$(POETRY) run isort asymmetric --check

pylint:
	$(POETRY) run pylint asymmetric

# Aggresive linters
black!:
	$(POETRY) run black asymmetric

isort!:
	$(POETRY) run isort asymmetric
