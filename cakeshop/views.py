from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from rest_framework.decorators import api_view
from .models import Order, Cake, Customer
from django.db.models import Q
from rest_framework.response import Response

def main_page(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
@api_view(['POST', 'GET'])
def register_order(request):
    try:
        order_info = json.loads(request.body.decode())
    except ValueError:
        return Response({"status": "not ok"})
    customer, created = Customer.objects.get_or_create(
        phonenumber=order_info['Phone'],
        defaults={'email': order_info['Email'],
                  'name': order_info['Name'],
                  'address': order_info['Address']}
    )
    if not created:  # Обновляем информацию о клиенте
        customer.email = order_info['Email']
        customer.name = order_info['Name']
        customer.address = order_info['Address']
        customer.save()

    return Response({"status": 200})

    
   # Cake.objects.

    context = {}
    return render(request, 'index.html', context)