from django.contrib import admin
from django.db.models import Q

from cakeshop.models import Order, Customer, Cake, Decoration, Topping, Shape, Advertisement, Berry, Height


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = 'customer', 'cake'
    list_filter = 'status', 'delivery_address', 'delivery_datetime'
    list_display = 'customer', 'cake', 'delivery_address', 'delivery_datetime', 'status'
    list_editable = 'status',


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = 'name', 'email', 'phonenumber',


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = 'name', 'height', 'shape', 'topping', 'berry', 'decoration', 'price'
    list_editable = 'height', 'shape', 'topping', 'berry', 'decoration'

    def price(self, obj):
        Cake.add_price(obj)
        return obj.price

    price.short_description = 'цена'


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = 'title', 'start_date', 'quantity_total', 'quantity_paid', 'total_sold',

    def quantity_total(self, obj):
        obj.quantity_total = len([order for order in obj.orders.filter(Q(status='В обработке') |
                                                                       Q(status='Ожидает оплаты'))])
        return obj.quantity_total

    def quantity_paid(self, obj):
        obj.quantity_paid = len([order for order in obj.orders.filter(Q(status='Готовится') |
                                                                      Q(status='Доставлен'))])
        return obj.quantity_paid

    def total_sold(self, obj):
        obj.total_sold = sum([order.price for order in obj.orders.all()])
        return obj.total_sold

    quantity_total.short_description = 'Общее количество заказов по акции'
    quantity_paid.short_description = 'Количество оплаченных заказов'
    total_sold.short_description = 'Доход руб.'


@admin.register(Height)
class HeightAdmin(admin.ModelAdmin):
    pass


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    pass


@admin.register(Decoration)
class DecorationAdmin(admin.ModelAdmin):
    pass
