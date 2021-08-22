from django.contrib import admin
from django.urls import path

from core.views import index, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-email/', index, name='send_email'),
    path('', home, name='home'),
]