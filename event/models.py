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

# Create your models here.
class Categories(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)

    def __str__(self):
        return str(self.title) + " Title: " + self.title

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
    location = models.PointField()
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    image = models.FileField(upload_to='Events/%Y/%m/%d/', blank=True, null=True)  
    startdate = models.DateField(auto_now_add=False)
    starttime = models.TimeField(auto_now_add=False)
    enddate = models.DateField(auto_now_add=False)
    endtime = models.TimeField(auto_now_add=False)
    details = models.TextField(null=True, blank=True)
    
    EVENT_CHOICES = (
        ('0', 'In Person'),
        ('1', 'Virtual'),
    )
    eventtype = models.CharField(max_length=1, blank=True, null=True, choices=EVENT_CHOICES)
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