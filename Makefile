check: check-format check-lint

check-format:
	uv run ruff format . --diff

check-lint:
	uv run ruff check .

install: setup-git-hooks
	uv lock --locked
	uv sync --locked --group dev --group lint --group test

lint:
	uv run ruff format .
	uv run ruff check . --fix

run:
	uv run streamlit run src/app/main.py

test:
	uv run pytest -v --cov=src --cov-report=xml

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	git config core.hooksPath hooks