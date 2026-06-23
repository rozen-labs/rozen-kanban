#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput

if [[ -n "${BOOTSTRAP_ADMIN_USERNAME:-}" && -n "${BOOTSTRAP_ADMIN_EMAIL:-}" && -n "${BOOTSTRAP_ADMIN_PASSWORD:-}" ]]; then
  python manage.py bootstrap_admin             --username "$BOOTSTRAP_ADMIN_USERNAME"             --email "$BOOTSTRAP_ADMIN_EMAIL"             --password "$BOOTSTRAP_ADMIN_PASSWORD"
fi

python manage.py collectstatic --noinput

exec gunicorn kanban.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}" --timeout "${GUNICORN_TIMEOUT:-60}"
