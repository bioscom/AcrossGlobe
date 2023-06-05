from django.contrib import admin
from .models import *
import datetime
from django.conf import settings

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'is_approved', 'dateTime')
    list_filter=('is_approved', 'author', 'dateTime')

admin.site.register(TypeCategories)
admin.site.register(BlogPostCategories)
admin.site.register(Advertisement)
@admin.register(BlogPostSubCategories)
class BlogPostSubCategoriesAdmin(admin.ModelAdmin):
    list_display=('title', 'moderatoremail', 'sub_title')
    
    
admin.site.register(Comment)
