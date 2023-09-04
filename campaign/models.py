from django.db import models
from myblog.models import *
from datetime import datetime
from io import BytesIO
import sys
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ImageField
from django.urls import reverse
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
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

import secrets
from django.db.models.signals import post_save

import base64
import os
from uuid import uuid4


# Create your models here.
####################### Advertisement Module ###########################

def renameadfiles(instance, filename):
    #upload_to = 'adverts/%Y/%m/%d/'
    upload_to = 'adverts'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True, db_index=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True, db_index=True)
    image = models.FileField(upload_to=renameadfiles, blank=True, null=True)
    urllink = models.URLField(_('urllink'), max_length=255)
    status = models.CharField(max_length=20) # status turns expired when end_date is reached
    is_approved = models.BooleanField(default=False)
    duration = models.IntegerField(default=0, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, db_index=True)

    #class Meta:
    #    ordering=['-creation_date']

class PlaceAdvert(models.Model):
    advert = models.ForeignKey(Advertisement, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE, blank=True, null=True)
    adslot = models.IntegerField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, db_index=True)
    ordering = models.IntegerField(blank=True, null=True)
    

class AdvertCredit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    credit = models.DecimalField(max_digits = 20, decimal_places = 2)
    creation_date = models.DateField(auto_now_add=True, db_index=True)
    modified_date = models.DateField(auto_now_add=False, db_index=True)


class UniqueCodes(models.Model):
    """
    Class to create human friendly gift/coupon codes.
    """

    # Model field for our unique code
    code = models.CharField(max_length=8, blank=True, null=True, unique=True)
    is_redeemed = models.BooleanField(default=False)
    credit = models.DecimalField(_('credit'), max_digits=10, decimal_places=2, default=0)
    discount_rate = models.DecimalField(_('discount'), max_digits=8, decimal_places=2, default=0)
    
    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        """
        Connected to the post_save signal of the UniqueCodes model. This is used to set the
        code once we have created the db instance and have access to the primary key (ID Field)
        """
        # If new database record
        if created:
            # We have the primary key (ID Field) now so let's grab it
            id_string = str(instance.id)
            # Define our random string alphabet (notice I've omitted I,O,etc. as they can be confused for other characters)
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            # Create an 8 char random string from our alphabet
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            # Append the ID to the end of the random string
            instance.code = (random_str + id_string)[-8:]
            # Save the class instance
            instance.save()
    
    def __str__(self):
        return "%s" % (self.code)
    
# Connect the post_create function to the UniqueCodes post_save signal
#post_save.connect(Gift.post_create, sender=UniqueCodes)
#post_save.connect(Gift.post_create, sender=UniqueCodes)

######################################################################