web: gunicorn ecommerce.wsgi
release: python manage.py migrate
worker: celery -A ecommerce worker -l info
