import tarfile
from io import BytesIO

import requests
from django.core.management import BaseCommand

from eventowl.settings import GEOIP_PATH

GEOLITE_URL = 'https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz'


def download():
    resp = requests.get(GEOLITE_URL)
    resp.raise_for_status()
    with tarfile.open(fileobj=BytesIO(resp.content)) as t:
        for member in t:
            if member.name.endswith('.mmdb'):
                f = t.extractfile(member)
                with open(GEOIP_PATH, 'wb') as target:
                    target.write(f.read())


class Command(BaseCommand):
    help = 'Update geoip database'

    def handle(self, *args, **options):
        download()
