# Generated by Django 2.0.4 on 2018-04-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concertowl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='picture',
            field=models.ImageField(default='artist/default.jpg', upload_to='artist'),
        ),
        migrations.AddField(
            model_name='event',
            name='picture',
            field=models.ImageField(default='event/default.jpg', upload_to='event'),
        ),
    ]
