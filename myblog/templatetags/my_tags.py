from django import template
import re
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from ..models import BlogPost, SubBlogPost

register = template.Library()


@register.filter()
def highlight_yellow(text, value):
    if text is not None:
        text = str(text)
        src_str = re.compile(value, re.IGNORECASE)
        str_replaced = src_str.sub(f"<span class=\"highlight\">{value}</span>", text)
    else:
        str_replaced = ''

    return mark_safe(str_replaced)


@register.simple_tag()
def total_users():
    return User.objects.count()


@register.simple_tag()
def total_posts():
    totalposts = BlogPost.objects.filter(parent_id__isnull=True).count() + SubBlogPost.objects.filter(parent_id__isnull=True).count()
    return totalposts

# @register.simple_tag()
# def total_subposts():
#     return 