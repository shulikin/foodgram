echo 'Migrations...'
python manage.py migrate
echo 'Static...'
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8080 foodgram.wsgi  

exec "$@"