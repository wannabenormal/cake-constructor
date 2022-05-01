from django.contrib import admin
from cakeshop.models import Order, Customer, Cake, Decoration, Topping, Shape, Advertisement, Berry, Height


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = 'customer', 'cake'
    list_filter = 'status', 'delivery_address', 'delivery_datetime'
    list_display = 'customer', 'cake', 'delivery_address', 'delivery_datetime', 'status'
    list_editable = 'status',


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = 'referral',
    list_display = 'name', 'email', 'phonenumber', 'referral'
    list_filter = 'referral',


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
