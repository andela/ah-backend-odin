web: gunicorn authors.wsgi --log-file -
release: python manage.py makemigrations --noinput && python manage.py makemigrations password_reset_token && python manage.py migrate --noinput
