dev-sync:
    uv sync --all-extras --cache-dir .uv_cache

prod-sync:
	uv sync --all-extras --no-dev --cache-dir .uv_cache

format:
	uv run ruff format

lint:
    uv run ruff check --fix --exclude tests

test *OPTIONS:
	uv run pytest {{OPTIONS}} --color=yes tests

validate: format lint test

dockerize:
    docker build -t de_solution . -f Dockerfile

run *OPTIONS:
	uv run fastapi run de_solution/main.py --port 8080 {{OPTIONS}}

dev *OPTIONS:
	uv run fastapi dev de_solution/main.py --port 8080 {{OPTIONS}}

docker:
    cd "$(git rev-parse --show-toplevel)"
    docker build -t de_solution . -f Dockerfile
    docker run -p 8080:8080 de_solution:latest
