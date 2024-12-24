from django.contrib import admin
from django.urls import include
from django.urls import path
from web_dz_123 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('web_dz_123.urls'), name = 'index'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)