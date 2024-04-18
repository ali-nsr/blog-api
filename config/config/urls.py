from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
]

from django.conf import settings as conf_settings
from django.conf.urls.static import static

if conf_settings.DEBUG:
    urlpatterns += static(conf_settings.STATIC_URL, document_root=conf_settings.STATIC_ROOT)
    urlpatterns += static(conf_settings.MEDIA_URL, document_root=conf_settings.MEDIA_ROOT)