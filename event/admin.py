from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *
import datetime
from django.conf import settings

@admin.register(events)
class eventsAdmin(OSMGeoAdmin):
    list_display = ('eventname', 'location')

admin.site.register(Categories)
#@admin.register(events)
# class eventsAdmin(admin.ModelAdmin):
#     list_display=('title', 'author', 'is_approved', 'dateTime')
#     list_filter=('is_approved', 'author', 'dateTime')
