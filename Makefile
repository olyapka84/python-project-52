install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

start:
	uv run python manage.py runserver 0.0.0.0:8000

start-server:
	uv run python manage.py runserver 0.0.0.0:3000

render-start:
	uv run gunicorn task_manager.wsgi

build:
	./build.sh

lint:
	uv run ruff check --fix

test:
	uv run pytest -v
