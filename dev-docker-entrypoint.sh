#!/bin/bash

echo "Check for new migrations"
python3 manage.py makemigrations

echo "Apply database migrations"
python3 manage.py migrate

echo "Start built-in dev server"
python3 manage.py runserver 0.0.0.0:8000
