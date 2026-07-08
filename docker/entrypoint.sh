#!/bin/sh
set -e

APP_PORT="${APP_PORT:-8000}"
DJANGO_ENV="${DJANGO_ENV:-development}"
GUNICORN_WORKERS="${GUNICORN_WORKERS:-3}"
GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-120}"

python - <<'PY'
import os
import socket
import time

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))

for attempt in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        if attempt == 59:
            raise
        time.sleep(2)
PY

python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "production" ]; then
    python manage.py collectstatic --noinput
    exec gunicorn newfri.wsgi:application \
        --bind "0.0.0.0:${APP_PORT}" \
        --workers "${GUNICORN_WORKERS}" \
        --timeout "${GUNICORN_TIMEOUT}" \
        --access-logfile - \
        --error-logfile -
fi

exec python manage.py runserver "0.0.0.0:${APP_PORT}"
