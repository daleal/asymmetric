POETRY = $(shell which poetry)
POETRY_VERSION = 1.1.2

# Env stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --version $(POETRY_VERSION)

.PHONY: venv-with-dependencies
venv-with-dependencies:
	python3 -m venv .venv
	$(POETRY) run pip install --upgrade pip
	$(POETRY) run poetry install

# Passive linters
.PHONY: black
black:
	$(POETRY) run black asymmetric --check

.PHONY: flake8
flake8:
	$(POETRY) run flake8 asymmetric

.PHONY: isort
isort:
	$(POETRY) run isort asymmetric --check

.PHONY: pylint
pylint:
	$(POETRY) run pylint asymmetric

# Aggresive linters
.PHONY: black!
black!:
	$(POETRY) run black asymmetric

.PHONY: isort!
isort!:
	$(POETRY) run isort asymmetric

# Aggregated
.PHONY: linters
linters:
	$(MAKE) isort
	$(MAKE) black
	$(MAKE) flake8
	$(MAKE) pylint

.PHONY: linters!
linters!:
	$(MAKE) isort!
	$(MAKE) black!
	$(MAKE) flake8
	$(MAKE) pylint
