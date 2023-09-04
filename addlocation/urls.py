from django.contrib import admin
from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

from addlocation.views import addpoint,viewpoints,allpoints
urlpatterns = [
    #path(_('admin/'), admin.site.urls),
    path(_('addlocation/addlocation'),views.addpoint,name='addpoint'),
    path(_('addlocation/viewpoints'),views.viewpoints,name='viewpoints'),
    path(_('addlocation/allpoints'),views.allpoints,name='allpoints'),
]