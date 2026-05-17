release: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput && python manage.py populate_data
web: gunicorn yasemin_salon.wsgi
