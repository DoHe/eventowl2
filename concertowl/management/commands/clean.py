from datetime import datetime, timedelta

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from concertowl.models import Event, Notification


def clean(model, field, days):
    time_ago = datetime.now() - timedelta(days=days)
    model.objects.filter(**{field + '__lt': time_ago}).delete()


class Command(BaseCommand):
    help = 'Delete old entries'

    def handle(self, *args, **options):
        clean(Event, 'start_time', 14)
        clean(User, 'last_login', 30)
        clean(Notification, 'created', 30)
        LogEntry.objects.all().delete()
