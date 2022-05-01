from django.urls import include, path
from .views import (main_page,
                    register_order,
                    personal,
                    session,
                    success_payment,
                    cancel_payment,
                    create_order_form)
from django.views.generic.base import RedirectView

app_name = "cakeshop"

urlpatterns = [
    path('', main_page, name='main_page',),
    path('register_order/', register_order, name='register_order'),
    path('personal/', personal, name='personal'),
    path('create-checkout-session/<int:order_id>', session, name='create-checkout-session'),
    path('cancel/<int:order_id>', cancel_payment, name='cancel'),
    path('success/<int:order_id>', success_payment, name='success'),
    path('create_order/', create_order_form, name='create_order_form')
]
