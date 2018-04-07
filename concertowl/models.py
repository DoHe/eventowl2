from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='artist', default='artist/default.jpg')

    def __str__(self):
        return self.name


class Event(models.Model):
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    ticket_url = models.URLField()
    picture = models.ImageField(upload_to='event', default='event/default.jpg')
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return "{} at {} on {}".format(", ".join(artist.name.title() for artist in self.artists.all()),
                                       str(self.venue),
                                       str(self.date_time.strftime("%Y-%m-%d")))
