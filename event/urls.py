from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'event'

urlpatterns = [
    # previous login view
    path('events/', views.events_list, name='events_list'),
    path('newevent/', views.add_event, name="add_event"),
    path('events/<int:cat_id>/', views.event_list_by_category, name='event_list_by_category'),
    path('events/<int:id>/', views.event_detail, name="event_detail"), 
]