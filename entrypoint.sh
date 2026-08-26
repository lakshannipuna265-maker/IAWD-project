#!/bin/bash
set -e

echo "Waiting for database..."
python << END
import os, sys, time
import psycopg2

for i in range(30):
    try:
        psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "financetracker"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", ""),
            host=os.environ.get("DB_HOST", "db"),
            port=os.environ.get("DB_PORT", "5432"),
        )
        sys.exit(0)
    except psycopg2.OperationalError:
        time.sleep(1)
sys.exit(1)
END

echo "Database is ready. Applying migrations..."
python manage.py migrate

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
