#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install all dependencies from requirements
pip install -r requirements.txt

# 2. Collect static files for design styling
python manage.py collectstatic --noinput

# 3. AUTOMATIC MIGRATIONS: This updates your PostgreSQL database tables
python manage.py migrate