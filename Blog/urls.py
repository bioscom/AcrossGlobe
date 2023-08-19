
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# Change the header of the admin panel. 
admin.site.site_header = 'Across Globe Admin Panel'
admin.site.index_title = 'Customize App'

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('myblog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(_('account/'), include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    #path(r'^convert/', include('lazysignup.urls')),
    path('verification/', include('verify_email.urls')),
    path('ads/', include('ads.urls')),
    path(_('shop/'), include('shop.urls')),
    path(_('event/'), include('event.urls')),
    path(_('addlocation/'), include('addlocation.urls')),
) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
