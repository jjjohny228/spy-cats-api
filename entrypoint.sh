#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py migrate

# run web server
python manage.py runserver 0.0.0.0:8000