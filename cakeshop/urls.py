from django.urls import include, path
from .views import (main_page,
                    register_order,
                    personal,
                    session,
                    SuccessView,
                    CancelView,)
from django.views.generic.base import RedirectView

app_name = "cakeshop"

urlpatterns = [
    path('', main_page, name='main_page',),
    path('register_order/', register_order, name='register_order'),
    path('personal/', personal, name='personal'),
    path('create-checkout-session/<int:order_id>', session, name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('succes/', SuccessView.as_view(), name='success'),
]
