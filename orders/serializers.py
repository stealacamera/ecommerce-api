from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order
from products.serializers import MiniProductSerializer
from cart.models import CartItem
from users.serializers import AddressSerializer


class CheckoutSerializer(serializers.Serializer):
    def save(self):
        customer = self.context['request'].user
        user_cart = CartItem.objects.filter(user=customer)

        for item in user_cart:
            product = item.product
            
            if product.stock == 0:
                raise serializers.ValidationError(f'{product.name} is out of stock')
            elif product.stock < item.quantity:
                raise serializers.ValidationError(f'{product.name} doesn\'t have enough stock')
            else:
                product.stock = product.stock - item.quantity
                product.save()
            
            Order.objects.create(customer=customer,
                                 product=product,
                                 quantity=item.quantity)

        user_cart.delete()


class OrderSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source='product.seller', read_only=True)
    product = MiniProductSerializer(read_only=True)
    
    class Meta:
        model = Order
        exclude = ['customer']
        read_only_fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address']
 
class SalesSerializer(OrderSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['quantity']