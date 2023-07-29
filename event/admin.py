from django.contrib import admin
from .models import *
import datetime
from django.conf import settings

admin.site.register(events)
admin.site.register(Categories)
#@admin.register(events)
# class eventsAdmin(admin.ModelAdmin):
#     list_display=('title', 'author', 'is_approved', 'dateTime')
#     list_filter=('is_approved', 'author', 'dateTime')
