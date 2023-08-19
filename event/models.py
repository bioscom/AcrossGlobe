from django.db import models
from datetime import datetime
from io import BytesIO
import sys
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ImageField
from django.urls import reverse
from django.utils.timezone import now
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from django.utils.translation import gettext_lazy as _
from django.conf.locale.en import formats as en_formats
from requests import Session
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis import forms


# Create your models here.
class Categories(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('event:event_list_by_category', args=[self.id])


class events(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    eventname = models.CharField(_('eventname'), max_length=255)
    eventvenue = models.CharField(_('eventvenue'), blank=True, null=True, max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    image = models.FileField(upload_to='Events/%Y/%m/%d/', blank=True, null=True)  
    startdate = models.DateField(auto_now_add=False)
    starttime = models.TimeField(auto_now_add=False)
    enddate = models.DateField(auto_now_add=False, blank=True, null=True)
    endtime = models.TimeField(auto_now_add=False, blank=True, null=True)
    details = models.TextField(null=True, blank=True)
    
    EVENT_CHOICES = (
        ('0', 'In Person'),
        ('1', 'Virtual'),
    )
    eventtype = models.CharField(max_length=1, blank=True, null=True, choices=EVENT_CHOICES)
    #location = models.PointField(srid=4326, blank=True, null=True)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    #location = models.PointField(widget= forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    virtual_type = models.CharField(max_length=1, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_liked', blank=True)
    #hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return str(self.author) + " Event Name: " + self.eventname

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.eventname + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event:event_detail', args=[self.id])

    def get_id(self):
        return self.id
    
    class Meta:
        ordering=['-datetime']
        
    @property
    def longitudes(self):
        return self.location.x
    
    @property
    def latitudes(self):
        return self.location.y
    


class Place(models.Model):
   name = models.CharField(max_length=20)
   coord = models.PointField(blank=True, null=True)

   def __str__(self):
      return self.name