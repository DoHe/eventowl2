# Generated by Django 2.0.5 on 2018-05-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concertowl', '0017_userprofile_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='spotify_import_running',
            field=models.BooleanField(default=False),
        ),
    ]
