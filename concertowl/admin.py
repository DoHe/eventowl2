from django.contrib import admin

from .models import Artist, Event, Notification, UserProfile


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)


admin.site.register(Artist)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(UserProfile, ReadOnlyAdmin)
