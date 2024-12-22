from django.contrib import admin
from django.urls import include
from django.urls import path
from web_dz_123 import views

urlpatterns = [
    path('', include('web_dz_123.urls'), name = 'index'),
    path('admin/', admin.site.urls),
]
