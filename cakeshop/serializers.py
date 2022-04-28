from rest_framework.serializers import ModelSerializer
from cakeshop.models import Order, Customer, Cake


class CakeSerializer(ModelSerializer):

    class Meta:
        model = Cake
        fields = ['name', 'description', 'height', 'shape', 'topping', 'berry', 'decoration', 'inscription']

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Customer.objects.update(**validated_data)


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phonenumber', 'address']

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Customer.objects.update(**validated_data)


class OrderSerializer(ModelSerializer):

    customer = CustomerSerializer(allow_null=False)
    cake = CakeSerializer(allow_null=False)

    class Meta:
        model = Order
        fields = ['status',
                  'price',
                  'creation_time',
                  'delivery_datetime',
                  'delivery_address',
                  'comment',
                  'is_urgent',
                  'customer',
                  'cake']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)

# TODO add serializers for every model related to cake
