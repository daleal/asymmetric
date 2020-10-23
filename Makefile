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
	$(POETRY) run flake8 asymmetric --config=linters/flake8.cfg

.PHONY: isort
isort:
	$(POETRY) run isort asymmetric --profile=black --check

.PHONY: mypy
mypy:
	$(POETRY) run mypy asymmetric --config-file=linters/mypy.cfg

.PHONY: pylint
pylint:
	$(POETRY) run pylint asymmetric --rcfile=linters/pylint.cfg

# Aggresive linters
.PHONY: black!
black!:
	$(POETRY) run black asymmetric

.PHONY: isort!
isort!:
	$(POETRY) run isort asymmetric --profile=black

# Aggregated
.PHONY: linters
linters:
	$(MAKE) isort
	$(MAKE) black
	$(MAKE) flake8
	$(MAKE) mypy
	$(MAKE) pylint

.PHONY: linters!
linters!:
	$(MAKE) isort!
	$(MAKE) black!
	$(MAKE) flake8
	$(MAKE) mypy
	$(MAKE) pylint
