from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from concertowl.models import Event, Notification


def clean(model, field, days):
    time_ago = datetime.now() - timedelta(days=days)
    model.objects.filter(**{field + '__lt': time_ago}).delete()


class Command(BaseCommand):
    help = 'Delete old entries'

    def handle(self, *args, **options):
        clean(Event, 'start_time', 14)
        clean(User, 'last_login', 180)
        clean(Notification, 'created', 30)
