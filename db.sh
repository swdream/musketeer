#!/bin/bash
set -e

python manage.py makemigrations
python manage.py migrate
