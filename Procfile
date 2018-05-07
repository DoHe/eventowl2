release: python3 manage.py migrate --noinput && if [ `date +%d` = 01 ]; then python3 manage.py cities_light --progress; fi
web: gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
