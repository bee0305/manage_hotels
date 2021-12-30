from re import template
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
    path('ajax_select/', include(ajax_select_urls)),
    path('admin/', admin.site.urls), 
    path('',TemplateView.as_view(template_name='home.html')),
    path('cities/',include('city.urls')),   
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()