release: npm run build && python3 manage.py migrate --noinput && python3 manage.py cities_light
web: gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
