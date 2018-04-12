from django import templatetags
from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    picture = models.URLField(default=templatetags.static.static('default_artist.jpg'))
    description = models.TextField(blank=True, default="")
    url = models.URLField(blank=True, default="")
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'name': self.name,
            'picture_url': self.picture,
            'description': self.description,
            'url': self.url
        }


class Event(models.Model):
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    ticket_url = models.URLField()
    picture = models.URLField(default=templatetags.static.static('default_event.jpg'))
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return "{} at {} on {}".format(", ".join(artist.name.title() for artist in self.artists.all()),
                                       str(self.venue),
                                       str(self.date_time.strftime("%Y-%m-%d")))
