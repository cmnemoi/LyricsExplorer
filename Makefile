check:
	uv run ruff format . --diff

install: setup-git-hooks
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

lint:
	ruff format .
	ruff check . --fix

run:
	streamlit run src/app/main.py

test:
	uv run pytest -v --cov=src

setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	git config core.hooksPath hooks