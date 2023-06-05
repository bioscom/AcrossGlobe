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


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
#     image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
#     bio = models.TextField(_('bio'), blank=True, null=True)
#     phone_no = models.IntegerField(_('phone_no'), blank=True, null=True)
#     facebook = models.CharField(_('facebook'), max_length=300, blank=True, null=True)
#     instagram = models.CharField(_('instagram'), max_length=300, blank=True, null=True)
#     linkedin = models.CharField(_('linkedin'), max_length=300, blank=True, null=True)

#     def __str__(self):
#         return str(self.user)


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


class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')  # models.TextField()
    image = models.ImageField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)
    thumbnails=models.ImageField(upload_to='thumbnails/%Y/%m/%d/', blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_posts', editable=False)
    #anonymous_viewers = models.ManyToManyField(django_session, related_name='anonymous_viewed_posts', editable=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('MyBlog:blog_details', kwargs={'slug': self.slug})

    def number_of_likes(self):
        return self.viewers.count()

    def get_id(self):
        return self.id


class SubBlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    subcategory = models.ForeignKey(BlogPostSubCategories, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=130, blank=True)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')  # models.TextField()
    image = models.ImageField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)
    thumbnails=models.ImageField(upload_to='thumbnails/%Y/%m/%d/', blank=True, null=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='viewed_sub_posts', editable=False)
    #anonymous_viewers = models.ManyToManyField(django_session, related_name='anonymous_viewed_posts', editable=False)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sub_posts_liked', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def __str__(self):
        return str(self.author) + " Blog Title: " + self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('MyBlog:blog_sub_details', kwargs={'slug': self.slug})

    def number_of_likes(self):
        return self.viewers.count()

    def get_id(self):
        return self.id


class FileUploads(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    file = models.FileField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)

class SubFileUploads(models.Model):
    post = models.ForeignKey(SubBlogPost, on_delete=models.CASCADE)
    file = models.FileField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)



# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
#     content = RichTextUploadingField(null=True, blank=True, config_name='default')
#     # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
#     dateTime = models.DateTimeField(default=now)

#     def __str__(self):
#         return self.user.username + " Comment: " + str(self.content)

    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # @property
    # def children(self):
    #     return Comment.objects.filter(parent_comment=self).reverse()

    # @property
    # def is_parent(self):
    #     if self.parent_comment is None:
    #         return True
    #     return False  

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost , on_delete=models.CASCADE)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')
    dateTime = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering=['-dateTime']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class SubComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(SubBlogPost , on_delete=models.CASCADE)
    content = RichTextUploadingField(null=True, blank=True, config_name='default')
    dateTime = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='subreplies')

    class Meta:
        ordering=['-dateTime']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return SubComment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class CommentFileUploads(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    file = models.FileField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)


class SubCommentFileUploads(models.Model):
    comment = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    file = models.FileField(upload_to="FileUploads/%Y/%m/%d/", blank=True, null=True)

# class ReplyComment(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
#     replier_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     reply_content = RichTextUploadingField(null=True, blank=True, config_name='default')
#     #reply_content = RichTextField(_('reply_content'), )
#     replied_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "'{}' replied with '{}' to '{}'".format(self.replier_name, self.reply_content, self.reply_comment)



####################### Advertisement Module ###########################

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(BlogPostCategories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="advert_pics/%Y/%m/%d/", blank=True, null=True)
    urllink = models.URLField(_('urllink'), max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    start_date = models.DateTimeField(auto_now_add=False, db_index=True)
    status = models.BooleanField(default=False)


######################################################################

# #from django.contrib.auth import get_user_model

# class Comment(models.Model):
#     CommentPost = models.ForeignKey(Blog , on_delete=models.CASCADE)
#     author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
#     content = models.TextField()
#     date_posted = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

#     class Meta:
#         ordering=['-date_posted']

#     def __str__(self):
#         return str(self.author) + ' comment ' + str(self.content)

#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self).reverse()

#     @property
#     def is_parent(self):
#         if self.parent is None:
#             return True
#         return False    



# === Codes to migrate models into database === #
# python manage.py makemigrations
# python manage.py migrate
