from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'shop'

urlpatterns = [
    
    path(_(''), views.product_list, name='product_list'),
    path(_('<slug:category_slug>/'), views.product_list, name='product_list_by_category'),
    path(_('<int:id>/<slug:slug>/'), views.product_detail, name='product_detail'),
    
]
