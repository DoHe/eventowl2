# Generated by Django 2.0.5 on 2018-05-21 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('concertowl', '0020_auto_20180510_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read_by',
            field=models.ManyToManyField(related_name='read_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
