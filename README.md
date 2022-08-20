Для запуска можно использовать gunicorn или uwsgi или их аналоги

gunicorn - wsgi-коннектор
pip install gunicorn
gunicorn run_wsgi:application

uwsgi
pip install uwsgi
uwsgi --http :8000 --wsgi-file run_wsgi.py