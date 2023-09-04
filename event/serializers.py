from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = events 
        fields = ('pk', 'category', 'author', 'eventname', 'eventvenue', 'image', 'startdate', 'starttime', 'enddate', 'endtime', 'details', 'eventtype', 'location', 'latitude', 'longitude', 'virtual_type',)
        
        
        
    