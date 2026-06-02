#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static
python manage.py collectstatic --noinput
python manage.py migrate
