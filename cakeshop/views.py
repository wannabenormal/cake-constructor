from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import Order, Cake, Customer, Height, Shape, Topping, Berry, Decoration
from .serializers import OrderSerializer
from django.conf import settings
from django.views.generic import TemplateView
import stripe
from django.shortcuts import get_object_or_404


def main_page(request):
    heights = Height.objects.all()
    shapes = Shape.objects.all()
    toppings = Topping.objects.all()
    berries = Berry.objects.all()
    decorations = Decoration.objects.all()

    context = {"heights":
                   {"heights_codenames": [height.height_codename for height in heights],
                    "heights_names": [height.height for height in heights],
                    "heights_prices": [height.price for height in heights]},
               "shapes":
                   {"shapes_codenames": [shape.shape_codename for shape in shapes],
                    "shapes_names": [shape.shape for shape in shapes],
                    "shapes_prices": [shape.price for shape in shapes]},
               "toppings":
                   {"toppings_codenames": [topping.topping_codename for topping in toppings],
                    "toppings_names": [topping.topping for topping in toppings],
                    "toppings_prices": [topping.price for topping in toppings]},
               "berries":
                   {"berries_codenames": [berry.berry_codename for berry in berries],
                    "berries_names": [berry.berry for berry in berries],
                    "berries_prices": [berry.price for berry in berries]},
               "decorations":
                   {"decorations_codenames": [decoration.decoration_codename for decoration in decorations],
                    "decorations_names": [decoration.decoration for decoration in decorations],
                    "decorations_prices": [decoration.price for decoration in decorations]},
               }
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


def create_order_form(request):
    order_data = dict(request.POST.items())
    print(dict(request.POST.items()))
    # {'lvls': '3', 'form': '3',
    # 'topping': '3', 'berries':
    # '4', 'decor': '5', 'words': '123114',
    # 'comment': '', 'name': 'Илья', 'phone':
    # '89870608786', 'email': 'viktoryisnear@gmail.com',
    # 'address': 'Дом', 'date': '22.22.22', 'time': '12:21',
    # 'csrfmiddlewaretoken': 'raHnzakSbl1j9AOvYvkkPN4h8MEM6rZALp1VZp3hMGOq4u9rQqEXSoGfPmZQsdVZ'}
    time = '2022-04-28 01:08:49.016151'
    customer, created = Customer.objects.get_or_create(
        phonenumber=order_data['phone'],
        defaults={'email': order_data['email'],
                  'name': order_data['name'],
                  'address': order_data['address']}
    )
    if not created:  # Обновляем информацию о клиенте
        customer.email = order_data['email']
        customer.name = order_data['name']
        customer.address = order_data['address']
        customer.save()
    cake = Cake.objects.create(
        height=Height.objects.get(height_codename=order_data['lvls']),
        shape=Shape.objects.get(shape_codename=order_data['form']),
        topping=Topping.objects.get(topping_codename=order_data['topping']),
        berry=Berry.objects.get(berry_codename=order_data.get('berries')),
        decoration=Decoration.objects.get(decoration_codename=order_data.get('decor')),
        inscription=order_data.get('words'),
    )
    Cake.add_price(cake)
    price = cake.price
    order = Order.objects.create(
        cake=cake,
        customer=customer,
        price=price,
        delivery_datetime=time,
        delivery_address=order_data['address'],
    )

    return redirect(reverse('cakeshop:create-checkout-session', kwargs={'order_id': order.id}))


def personal(request):
    current_user = request.user
    customer = Customer.objects.get_object_or_404(name=current_user)

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
              .filter(customer=customer))
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
    price = order.price
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': price,
                    'product_data': {
                        'name': f'Заказ №{order.id}, торт "{order.cake.name}"'
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
