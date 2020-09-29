#!/bin/bash

echo "Install requirements"
pip3 install -r requirements.txt

echo "Check for new migrations"
python3 manage.py makemigrations

echo "Apply database migrations"
python3 manage.py migrate

echo "Prepare app"
python3 manage.py prepare

echo "Start built-in dev server"
python3 manage.py runserver 0.0.0.0:8000
