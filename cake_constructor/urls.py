from django.urls import include, path
from django.contrib import admin

from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('cakeshop.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
