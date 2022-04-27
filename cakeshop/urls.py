from django.urls import include, path
from django.contrib import admin
from .views import view
from django.conf import settings
from django.conf.urls.static import static

app_name = "cakeshop"

urlpatterns = [
    path('', view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
