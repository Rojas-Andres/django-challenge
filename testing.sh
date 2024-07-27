#!/bin/sh

python3.11 manage.py migrate --noinput &

exec "$@"