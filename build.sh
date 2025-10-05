#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  . "$HOME/.local/bin/env"
else
  [ -f "$HOME/.local/bin/env" ] && . "$HOME/.local/bin/env"
fi

# 2) Установить зависимости (создаст .venv)
uv sync

# 3) Все django-команды — строго через uv run
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate
