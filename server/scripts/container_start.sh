#!/bin/bash

/usr/local/bin/wait-for-it.sh -t 30 db:5432

echo "FLASK_ENV:"
echo $FLASK_ENV
echo "**********"

echo "Running migrations"
flask db upgrade

if [ "$FLASK_ENV" = "DEVELOPMENT" ]; then
    echo "Running in development mode"
    exec flask run --reload
elif [ "$FLASK_ENV" = "PRODUCTION" ]; then
    echo "Running in production mode"
    exec gunicorn -b 0.0.0.0:5000 "app.create_app:create_app(mode='production')"
fi
