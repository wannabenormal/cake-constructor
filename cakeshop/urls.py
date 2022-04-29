from django.urls import include, path
from django.contrib import admin
from .views import main_page, register_order, personal
from django.conf import settings
from django.conf.urls.static import static

app_name = "cakeshop"

urlpatterns = [
    path('', main_page),
    path('register_order/', register_order),
    path('personal/', personal)
]
