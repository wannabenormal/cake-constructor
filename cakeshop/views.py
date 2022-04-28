from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from rest_framework.decorators import api_view
from .models import Order, Cake, Customer
from django.db.models import Q
from rest_framework.response import Response
from .serializers import OrderSerializer


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
                            "height": "1",
                            "shape": "1",
                            "topping": "1",
                            "berry": "1",
                            "decoration": "1",
                            "inscription": ""}
                   }

#@csrf_exempt
@api_view(['POST'])
def register_order(request):
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)

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
    Order.objects.create(
        cake=cake,
        customer=customer,
        price=order_serializer.validated_data['price'],
        delivery_datetime=order_serializer.validated_data['delivery_datetime'],
        delivery_address=order_serializer.validated_data['delivery_address'],
    )

    return Response({"status": 200})

    
   # Cake.objects.

    context = {}
    return render(request, 'index.html', context)


#  login required
def personal(request, user_id):
    customer = Customer.objects.get(id=user_id)  # TODO add 'with_orders' method
    name = customer.name
    email = customer.email
    phonenumber = customer.phonenumber
    orders = (Order.objects
              .prefetch_related('cake')
              .select_related('cake__shape')
              .select_related('cake__height')
              .select_related('cake__topping')
              .select_related('cake__berry')
              .select_related('cake__decoration')
              .filter(customer=customer))  # TODO add 'with_params' method
    order_details = []
    for order in orders:
        order_details.append({
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

    print(order_details)
    context = {}
    return render(request, 'lk.html', context)


