release: python3 manage.py migrate --noinput
web: newrelic-admin generate-config $NEW_RELIC_LICENSE_KEY newrelic.ini && NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
