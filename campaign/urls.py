from django.conf import settings
from django.urls import path, re_path as url
from . import views
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.contrib import admin


app_name = 'campaign'

urlpatterns = [
    #Advertisement
    path(_('campaign/'), views.campaign, name="campaign"),
    path(_('adverts/'), views.adverts, name="adverts"),                                                #   blog/partial_advertisement.html
    path(_('edit/<int:pk>'), views.edit_advertisement, name="edit"),
    path(_('myads/'), views.myads, name="myads"), 
    path(_('adslots/<int:pk>'), views.available_ads_slots, name="available_ads_slots"), 
    path(_('adrate/'), views.adrate, name="adrate"), 
    
    # Administrator
    path(_('all_ads/'), views.allads, name="all_ads"),  
    path(_('approval/<int:pk>'), views.approval, name="approval"),
    path(_('advertcredit/'), views.advertcredit, name="advertcredit"),
    path(_('addcredit/'), views.addcredit, name="addcredit"),
    path(_('updatecredit/<int:pk>'), views.updatecredit, name="updatecredit"),
    
    
    
    
]