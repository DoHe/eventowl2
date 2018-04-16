from django import templatetags
from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    picture = models.URLField(default=templatetags.static.static('default_artist.jpg'))
    description = models.TextField(blank=True, default="")
    url = models.URLField(blank=True, default="")
    subscribers = models.ManyToManyField(User, related_name='subscribers')

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
    title = models.CharField(max_length=200, blank=True, default="")
    venue = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, default="")
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    ticket_url = models.URLField()
    picture = models.URLField(default=templatetags.static.static('default_event.jpg'))
    artists = models.ManyToManyField(Artist, related_name='artists')

    def __str__(self):
        return "{} at {} on {}".format(str(self.title), str(self.venue), str(self.start_time.strftime("%Y-%m-%d")))

    def to_json(self):
        return {
            'title': self.title,
            'picture_url': self.picture,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'ticket_url': self.ticket_url,
            'venue': self.venue,
            'artists': [artist.name for artist in self.artists.all()]
        }
