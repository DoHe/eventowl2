release: python3 manage.py migrate --noinput && curl -s https://1a256929-6b46-4ede-a0e8-02c46006b7d9@www.hostedgraphite.com/agent/installer/deb/ | sudo sh
web: gunicorn eventowl.wsgi --log-file - -c gunicorn.conf
worker: python3 manage.py qcluster
