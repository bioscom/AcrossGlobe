from datetime import datetime
from io import BytesIO
import sys
from django.conf import settings
from django.db import models
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


class TypeCategories(models.Model):
    type = models.CharField(_('type'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.type

class BlogPostCategories(models.Model):
    type = models.ForeignKey(TypeCategories, default=1, on_delete=models.CASCADE)
    category_title = models.CharField(_('category_title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    moderatoremail = models.EmailField(_("email address"), blank=True)
    sub_title = models.CharField(_('sub_title'), max_length=355, blank=True)
    adrate = models.DecimalField(_('adrate'), max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(_('discount'), max_digits=8, decimal_places=2, default=0)
    
    DISCOUNT_CHOICES = (
        ('Discount', 'Discount'),
        ('Premium', 'Premium'),
    )
    discount_type = models.CharField(max_length=20, blank=True, null=True, choices=DISCOUNT_CHOICES)

    def __str__(self):
        return str(self.category_title) + " Category Title: " + self.category_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_title)
        super().save(*args, **kwargs)


class BlogPostSubCategories(models.Model):
    category = models.ForeignKey(BlogPostCategories, default=1, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    moderatoremail = models.EmailField(_("email address"), blank=True)
    sub_title = models.CharField(_('sub_title'), max_length=355, blank=True)
    adrate = models.DecimalField(_('adrate'), max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(_('discount'), max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

#Source: https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload
def renamefile(instance, filename):
    #upload_to = 'FileUploads/%Y/%m/%d/'
    upload_to = 'FileUploads'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def renamethumbnails(instance, filename):
    upload_to = 'thumbnails'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def renameadfiles(instance, filename):
    upload_to = 'advert_pics/%Y/%m/%d/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')  # models.TextField()
    image1 = models.FileField(upload_to=renamefile, blank=True, null=True)  
    image2 = models.FileField(upload_to=renamefile, blank=True, null=True)
    image3 = models.FileField(upload_to=renamefile, blank=True, null=True)
    image4 = models.FileField(upload_to=renamefile, blank=True, null=True)
    thumbnails=models.FileField(upload_to=renamethumbnails, blank=True, null=True, verbose_name='thumbnails')
    dateTime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_posts', editable=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        
        output_size = (250, 130)
        output_thumb = BytesIO()

        if self.image1:
            img = Image.open(self.image1)
            img_name = self.image1.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image2:
            img = Image.open(self.image2)
            img_name = self.image2.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image3:
            img = Image.open(self.image3)
            img_name = self.image3.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image4:
            img = Image.open(self.image4)
            img_name = self.image4.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)

        super(BlogPost, self).save()

    def get_absolute_url(self):
        return reverse('MyBlog:blog_details', kwargs={'slug': self.slug})

    def number_of_likes(self):
        return self.viewers.count()

    def get_id(self):
        return self.id
    
    class Meta:
        ordering=['-dateTime']
    
    
    
    @property
    def children(self):
        return BlogPost.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



class SubBlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    subcategory = models.ForeignKey(BlogPostSubCategories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')  # models.TextField()
    image1 = models.FileField(upload_to=renamefile, blank=True, null=True)  
    image2 = models.FileField(upload_to=renamefile, blank=True, null=True)
    image3 = models.FileField(upload_to=renamefile, blank=True, null=True)
    image4 = models.FileField(upload_to=renamefile, blank=True, null=True)
    thumbnails=models.FileField(upload_to=renamethumbnails, blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_sub_posts', editable=False)
    #anonymous_viewers = models.ManyToManyField(django_session, related_name='anonymous_viewed_posts', editable=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sub_posts_liked', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    
    
    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        
        output_size = (250, 130)
        output_thumb = BytesIO()

        if self.image1:
            img = Image.open(self.image1)
            img_name = self.image1.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image2:
            img = Image.open(self.image2)
            img_name = self.image2.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image3:
            img = Image.open(self.image3)
            img_name = self.image3.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)
                
        elif self.image4:
            img = Image.open(self.image4)
            img_name = self.image4.name.split('.')[0]
            if img.height > 250 or img.width > 250:
                img.thumbnail(output_size)
                img.save(output_thumb,format='JPEG',quality=90)
            self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)

        super(SubBlogPost, self).save()

    def get_absolute_url(self):
        return reverse('MyBlog:blog_sub_details', kwargs={'slug': self.slug})

    def number_of_likes(self):
        return self.viewers.count()

    def get_id(self):
        return self.id
    
    class Meta:
        ordering=['-dateTime']
    
    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title
    
    @property
    def children(self):
        return SubBlogPost.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False




class Paginating(models.Model):
    number_of_pages = models.IntegerField(default=0)


# === Codes to migrate models into database === #
# python manage.py makemigrations
# python manage.py migrate
