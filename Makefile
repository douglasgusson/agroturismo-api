.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site


.PHONY: install
install:          ## Install the project in dev mode.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[dev]

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort agroturismo_api/
	$(ENV_PREFIX)black -l 79 agroturismo_api/
	$(ENV_PREFIX)black -l 79 tests/


.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 agroturismo_api/
	$(ENV_PREFIX)black -l 79 --check agroturismo_api/
	$(ENV_PREFIX)black -l 79 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports agroturismo_api/


.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=agroturismo_api -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html
