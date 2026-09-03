#!/bin/sh
set -eu

chown -R appuser:appuser /app/staticfiles

exec gosu appuser /bin/sh -c 'python manage.py migrate --noinput; python manage.py collectstatic --noinput; exec "$@"' -- "$@"
