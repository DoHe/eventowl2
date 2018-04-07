from django.contrib import admin

from .models import Artist, Event

admin.site.register(Artist)
admin.site.register(Event)
