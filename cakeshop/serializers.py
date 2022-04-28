from rest_framework.serializers import ModelSerializer, RelatedField, ReadOnlyField, PrimaryKeyRelatedField
from cakeshop.models import Order, Customer, Cake, Shape, Topping, Decoration, Height, Berry


class CakeSerializer(ModelSerializer):
    height = PrimaryKeyRelatedField(read_only=False, queryset=Height.objects.all())
    shape = PrimaryKeyRelatedField(read_only=False, queryset=Shape.objects.all())
    topping = PrimaryKeyRelatedField(read_only=False, queryset=Topping.objects.all())
    decoration = PrimaryKeyRelatedField(read_only=False, queryset=Decoration.objects.all())
    berry = PrimaryKeyRelatedField(read_only=False, queryset=Berry.objects.all())

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
