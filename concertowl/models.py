import uuid

from django import templatetags
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class ArtistQuerySet(models.QuerySet):

    def _name_as_slug(self, kwargs):
        if 'name' in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
            del(kwargs['name'])
        return kwargs

    def get(self, *args, **kwargs):
        self._name_as_slug(kwargs)
        return super().get(*args, **kwargs)


class Artist(models.Model):
    name = models.CharField(max_length=200)
    picture = models.URLField(default=templatetags.static.static('default_artist.jpg'), max_length=500)
    description = models.TextField(blank=True, default="")
    url = models.URLField(blank=True, default="", max_length=500)
    subscribers = models.ManyToManyField(User, related_name='subscribers')
    slug = models.CharField(max_length=200)
    objects = ArtistQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        start_time = self.start_time if isinstance(self.start_time, str) else self.start_time.strftime("%Y-%m-%d")
        return "{} at {} on {}".format(
            str(self.title),
            str(self.venue),
            str(start_time)
        )

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
            'artists': [artist.name for artist in self.artists.all()],
            'event_id': self.id
        }


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='event')
    read_by = models.ManyToManyField(User, related_name='read_by')

    def to_json(self):
        j = {'created': self.created.isoformat()}
        j.update(self.event.to_json())
        return j


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    manual = models.BooleanField(default=False)
    spotify_import_running = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
