release: python3 manage.py migrate --noinput
web: gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
