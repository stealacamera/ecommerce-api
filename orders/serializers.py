from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order
from cart.models import CartItem
from users.serializers import AddressSerializer


class CheckoutSerializer(serializers.Serializer):
    def save(self):
        customer = self.context['request'].user
        user_cart = CartItem.objects.filter(user=customer)

        for item in user_cart:
            product = item.product
            seller = product.seller
            
            if product.stock == 0:
                raise serializers.ValidationError(f'{product.name} is out of stock')
            elif product.stock < item.quantity:
                raise serializers.ValidationError(f'{product.name} doesn\'t have enough stock')
            else:
                product.stock = product.stock - item.quantity
                product.save()
            
            Order.objects.create(seller=seller,
                                 customer=customer,
                                 product=product,
                                 quantity=item.quantity)

        user_cart.delete()


class OrderSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source='seller.username', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address']
 
class SalesSerializer(OrderSerializer):
    customer = CustomerSerializer(read_only=True)