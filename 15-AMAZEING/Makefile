SYSTEM_PYTHON ?= python3
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
CONFIG ?= config.txt

.PHONY: venv install run debug clean lint test demo check package

venv:
	@test -x "$(PYTHON)" || $(SYSTEM_PYTHON) -m venv "$(VENV)"

install: venv
	$(PIP) install -e ".[dev]"

run: install
	$(PYTHON) a_maze_ing.py "$(CONFIG)"

debug: install
	$(PYTHON) -m pdb a_maze_ing.py "$(CONFIG)"

clean:
	find . -path "./$(VENV)" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build

lint: install
	$(PYTHON) -m flake8 --ignore= --exclude="$(VENV)" .
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs . --exclude="$(VENV)"

test: install
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

demo: install
	$(PYTHON) -m tests.test_visualizer --demo

check: lint test

package: install
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m build --no-isolation --outdir .
	rm -rf build
