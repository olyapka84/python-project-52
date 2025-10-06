install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

start:
	uv run python manage.py runserver 0.0.0.0:8000

render-start:
	uv run gunicorn task_manager.wsgi

build:
	./build.sh

lint:
	uv run ruff check --fix

test:
	uv run pytest -v

.PHONY: start start-server

PORT ?= 3000

start-server:
	@if [ -f code/manage.py ]; then \
		cd code && uv run python manage.py runserver 0.0.0.0:$(PORT); \
	else \
		uv run python manage.py runserver 0.0.0.0:$(PORT); \
	fi

start:
	$(MAKE) start-server PORT=8000