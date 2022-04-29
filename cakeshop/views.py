import json
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Order, Cake, Customer
from rest_framework.response import Response
from .serializers import OrderSerializer
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
import stripe


def main_page(request):
    # TODO do list with cakes for main page?
    # TODO do dict with all cakes's parameters to display on main page
    context = {}
    return render(request, 'index.html', context)


drf_test_string = {"status": "В обработке",
                   "price": 500,
                   "delivery_datetime": "2022-04-28 01:08:49.016151",
                   "delivery_address": "Москва",
                   "customer": {
                       "name": "first",
                       "email": "validated@mail.ru",
                       "phonenumber": "89878888881",
                       "address": "Москва"
                   },
                   "cake": {"name": "Cake",
                            "description": "simple cake",
                            "height": "one",
                            "shape": "s",
                            "topping": "1",
                            "berry": "1",
                            "decoration": "1",
                            "inscription": ""}
                   }


@api_view(['POST'])
def register_order(request):
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=False)

    customer, created = Customer.objects.get_or_create(
        phonenumber=order_serializer.validated_data['customer']['phonenumber'],
        defaults={'email': order_serializer.validated_data['customer']['email'],
                  'name': order_serializer.validated_data['customer']['name'],
                  'address': order_serializer.validated_data['customer']['address']}
    )
    if not created:  # Обновляем информацию о клиенте
        customer.email = order_serializer.validated_data['customer']['email']
        customer.name = order_serializer.validated_data['customer']['name']
        customer.address = order_serializer.validated_data['customer']['address']
        customer.save()
    cake = Cake.objects.create(
        height=order_serializer.validated_data['cake']['height'],
        shape=order_serializer.validated_data['cake']['shape'],
        topping=order_serializer.validated_data['cake']['topping'],
        berry=order_serializer.validated_data['cake'].get('berry'),
        decoration=order_serializer.validated_data['cake'].get('decoration'),
        inscription=order_serializer.validated_data['cake'].get('inscription'),
    )
    order = Order.objects.create(
        cake=cake,
        customer=customer,
        price=order_serializer.validated_data['price'],
        delivery_datetime=order_serializer.validated_data['delivery_datetime'],
        delivery_address=order_serializer.validated_data['delivery_address'],
    )

    return redirect(reverse('cakeshop:create-checkout-session', kwargs={'order_id': order.id}))

   # context = {}
  #  return render(request, 'index.html', context)


#  login required
def personal(request):
    current_user = request.user
    customer = Customer.objects.get(name=current_user)  # TODO add 'with_orders' method

    customer_details = {
        'name': customer.name,
        'email': customer.email,
        'phonenumber': customer.phonenumber
    }

    orders = (Order.objects
              .prefetch_related('cake')
              .select_related('cake__shape')
              .select_related('cake__height')
              .select_related('cake__topping')
              .select_related('cake__berry')
              .select_related('cake__decoration')
              .filter(customer=customer))  # TODO add 'with_params' method
    orders_details = []
    for order in orders:
        orders_details.append({
            'id': order.id,
            'cake_name': order.cake.name,
            'status': order.status,
            'delivery_datetime': order.delivery_datetime,
            'height': order.cake.height,
            'shape': order.cake.shape,
            'topping': order.cake.topping,
            'berry': order.cake.berry,
            'decoration': order.cake.decoration,
            'inscription': order.cake.inscription,
        })

    context = {
        'orders': orders_details,
        'customer': customer_details
    }
    return render(request, 'lk.html', context)


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


stripe.api_key = settings.STRIPE_SECRET_KEY


def session(request, order_id):
    order = Order.objects.get(id=order_id)
    YOUR_DOMAIN = 'http://127.0.0.1:8000'

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2000,
                    'product_data': {
                        'name': 'test_payment_product'
                    }
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success',
        cancel_url=YOUR_DOMAIN + '/cancel',
    )
    return redirect(checkout_session.url, code=303)
    #return redirect('https://google.com', code=303)

