from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.decorators import api_view
import json
from .models import Order, Cake, Customer
from django.db.models import Q

def main_page(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
def register_order(request):
    order_info = json.loads(request.body)

    customer, created = Customer.objects.get_or_create(
        phonenumber=order_info['Phone'],
        defaults={'email': order_info['Email'],
                  'name' : order_info['Name'],
                  'address' : order_info['Address']}
    )
    if not created: # Обновляем информацию о клиенте
        customer.email = order_info['Email']
        customer.name = order_info['Name']
        customer.address = order_info['Address']
        customer.save()

    
   # Cake.objects.





    context = {}
    return render(request, 'index.html', context)