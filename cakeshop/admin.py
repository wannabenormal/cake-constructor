from django.contrib import admin
from cakeshop.models import Order, Customer, Cake, Decoration, Topping, Shape, Advertisement, Berry, Height


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = 'customer', 'cake'
    list_filter = 'status', 'delivery_address', 'delivery_datetime'
    list_display = 'customer', 'cake', 'delivery_address', 'delivery_datetime', 'status'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = 'referral',
    list_display = 'name', 'email', 'phonenumber', 'referral'
    list_filter = 'referral',


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    raw_id_fields = 'height', 'shape', 'topping', 'berry', 'decoration'
    list_display = 'name', 'height', 'shape',
    # TODO count cake's price and show it


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


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
