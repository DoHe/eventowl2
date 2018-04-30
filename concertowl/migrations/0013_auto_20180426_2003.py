# Generated by Django 2.0.4 on 2018-04-26 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concertowl', '0012_auto_20180422_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='picture',
            field=models.URLField(default='/static/default_artist.jpg', max_length=500),
        ),
        migrations.AlterField(
            model_name='artist',
            name='url',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
    ]