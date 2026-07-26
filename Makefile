.PHONY: install lint type-check test check links

install:
	python -m pip install -e '.[dev]'

lint:
	python -m ruff check .

type-check:
	python -m mypy src tests

test:
	python -m pytest

links:
	python tests/check_markdown_links.py

check: lint type-check test links
