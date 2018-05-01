release: python3 manage.py migrate --noinput && python3 manage.py update_geoip
web: gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
