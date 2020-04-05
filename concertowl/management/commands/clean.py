from datetime import datetime, timedelta

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from concertowl.models import Event, Notification


def clean(model, field, days, exceptions={}):
    time_ago = datetime.now() - timedelta(days=days)
    old = model.objects.filter(**{field + '__lt': time_ago})
    for field, values in exceptions.items():
        old = old.exclude(**{field + '__in': values})
    old.delete()


class Command(BaseCommand):
    help = 'Delete old entries'

    def handle(self, *args, **options):
        clean(Event, 'start_time', 14)
        clean(User, 'last_login', 30, {
            'username': [
                'eventowladmin',
                'eventowl2admin',
                'derdot'
            ]
        })
        clean(Notification, 'created', 30)
        LogEntry.objects.all().delete()
