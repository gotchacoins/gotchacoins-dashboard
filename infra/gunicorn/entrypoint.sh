#!/bin/bash

cd /server

# Starting Gunicorn - Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX
echo "Starting API app Gunicorn"

exec /venv/bin/gunicorn --bind 0.0.0.0:9000 --timeout 120 --workers 3 config.wsgi:application \
    --log-level=debug \
    --log-file=- \
    --access-logfile=- \
    --error-logfile=- \
    --capture-output

echo "Started Gunicorn"