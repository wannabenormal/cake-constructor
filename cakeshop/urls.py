from django.urls import include, path
from .views import (main_page,
                    register_order,
                    personal,
                    CreateCheckOutSessionView,
                    ProductLandingPageView,
                    SuccessView,
                    CancelView,)

app_name = "cakeshop"

urlpatterns = [
    path('', main_page),
    path('register_order/', register_order),
    path('personal/', personal),
    path('create-checkout-session', CreateCheckOutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('succes/', SuccessView.as_view(), name='success'),
    path('landing/', ProductLandingPageView.as_view(), name='landing-page'),
]
