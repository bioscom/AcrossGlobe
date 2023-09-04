from django.urls import path, re_path
#from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'event'

urlpatterns = [
    # previous login view
    path('events/', views.events_list, name='events_list'),
    path('newevent/', views.add_event, name="add_event"),
    path('events/<int:cat_id>/', views.event_list_by_category, name='event_list_by_category'),
    path('events/<str:slug>/', views.event_detail, name="event_detail"), 
    path('events/map/<str:slug>/', views.popup_map, name="popup_map"),
     #   Like and Unlike
    path(_('event/like/'), views.post_like, name='like'),    
    
    path('api/events/', views.events_list0),
    path('api/events/<str:slug>/', views.event_detail0),
    #re_path(r'^api/events/$', views.events_list0),
    #re_path(r'^api/events/([0-9])$', views.event_detail0),
]