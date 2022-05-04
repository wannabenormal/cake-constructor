from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, Cake, Customer, Height, Shape, Topping, Berry, Decoration, Advertisement
from .serializers import OrderSerializer
from django.conf import settings
import stripe
from django.shortcuts import get_object_or_404
import datetime


def main_page(request):
    utm_referral = request.GET.get('utm_referral')
    request.session['utm_referral'] = utm_referral
    heights = Height.objects.all()
    shapes = Shape.objects.all()
    toppings = Topping.objects.all()
    berries = Berry.objects.all()
    decorations = Decoration.objects.all()

    context = {
        "heights": [
            {"height_codename": height.height_codename,
             "height_name": height.height,
             "height_price": height.price} for height in heights],
        "shapes": [
            {"shape_codename": shape.shape_codename,
             "shape_name": shape.shape,
             "shape_price": shape.price} for shape in shapes],
        "toppings": [
            {"topping_codename": topping.topping_codename,
             "topping_name": topping.topping,
             "topping_price": topping.price} for topping in toppings],
        "berries": [
            {"berry_codename": berry.berry_codename,
             "berry_name": berry.berry,
             "berry_price": berry.price} for berry in berries],
        "decorations": [
            {"decoration_codename": decoration.decoration_codename,
             "decoration_name": decoration.decoration,
             "decoration_price": decoration.price} for decoration in decorations],
        "fast_date": datetime.datetime.now() + datetime.timedelta(days=1)
    }
    return render(request, 'index.html', context)


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
    if (order_serializer.validated_data['delivery_datetime'] - datetime.datetime.now(datetime.timezone.utc)).days < 1:
        is_urgent = True
    else:
        is_urgent = False
    Cake.add_price(cake)
    price = cake.price
    if is_urgent:
        price = price * 1.2

    Order.objects.create(
        cake=cake,
        customer=customer,
        price=price,
        delivery_datetime=order_serializer.validated_data['delivery_datetime'],
        delivery_address=order_serializer.validated_data['delivery_address'],
        comment=order_serializer.validated_data.get('comments')
    )

    return Response(order_serializer.data, status=201)


def create_order_form(request):
    request.session['is_payment'] = True
    order_data = dict(request.POST.items())
    date = "-".join(order_data['date'].replace('.', '-').split('-')[::-1])
    time = order_data['time']
    try:
        date_time = str(date + " " + time + ':00.000000')  # FIXME too much hardcode :)
    except Exception as e:
        print(e)
        date_time = '2022-05-03 00:00:00.016151'

    if (datetime.datetime.fromisoformat(date_time) - datetime.datetime.now()).days < 1:
        is_urgent = True
    else:
        is_urgent = False
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
        shape=Shape.objects.get(shape_codename=order_data['shape']),
        topping=Topping.objects.get(topping_codename=order_data['topping']),
        berry=Berry.objects.get(berry_codename=order_data.get('berries')),
        decoration=Decoration.objects.get(decoration_codename=order_data.get('decor')),
        inscription=order_data.get('words'),
    )
    Cake.add_price(cake)
    price = cake.price
    if is_urgent:
        price = price * 1.2

    order = Order.objects.create(
        cake=cake,
        customer=customer,
        price=price,
        delivery_datetime=date_time,
        delivery_address=order_data['address'],
        comment=order_data.get('comment'),
        is_urgent=is_urgent
    )

    return redirect(reverse('cakeshop:create-checkout-session', kwargs={'order_id': order.id}))


def personal(request):
    if not request.user.is_authenticated:
        return redirect('../accounts/login/')

    current_user = request.user
    customer = current_user.customer.first()
    if not customer:
        return redirect('../accounts/login/')

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


def success_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not request.session.get('is_payment') or order.status != 'Ожидает оплаты':
        return redirect(reverse('cakeshop:main_page'))

    order.status = 'Готовится'
    order.save()

    return redirect(reverse('cakeshop:main_page'))


def cancel_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Ожидает оплаты'
    order.save()
    return render(request, 'cancel.html')


stripe.api_key = settings.STRIPE_SECRET_KEY


def session(request, order_id):
    if not request.session.get('is_payment'):
        return redirect(reverse('cakeshop:main_page'))

    utm_referral = request.session.get('utm_referral')

    order = Order.objects.get(id=order_id)
    order.status = 'Ожидает оплаты'
    if utm_referral:
        advertisement = Advertisement.objects.filter(title=utm_referral).first()
        if advertisement:
            order.referral = advertisement
    order.save()
    my_domain = settings.SERVER_IP_OR_DOMAIN
    price = order.price
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': price * 100,
                    'product_data': {
                        'name': f'Заказ №{order.id}, торт "{order.cake.name}"'
                    }
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=my_domain + '/success/' + str(order_id),
        cancel_url=my_domain + '/cancel/' + str(order_id),
    )
    return redirect(checkout_session.url, code=303)
