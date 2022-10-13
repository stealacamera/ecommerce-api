from rest_framework import serializers

from .models import CartItem
from products.models import Product
from products.serializers import MiniProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = MiniProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'quantity', 'total']
        extra_kwargs = {'quantity': {'required': True}}
    
    def get_total(self, obj):
        return obj.quantity * obj.product.price
    
    def validate(self, attrs):      
        # Get the product in the cart item
        if self.context['request'].method == 'POST':
            product_pk = self.context['product_pk']
            product = Product.objects.get(id=product_pk)
            cart_user = self.context['request'].user
            
            # Check if the product is the user's
            if product.seller == cart_user:
                raise serializers.ValidationError('You cannot order your own product')
            
            # Check if product is already in the cart
            if CartItem.objects.filter(user=cart_user,
                                       product_id=product_pk).exists():
                raise serializers.ValidationError('You have already added this product to the cart')
        else:
            product = Product.objects.get(id=self.instance.product_id)
        
        # Check if quantity exceeds product stock
        if attrs['quantity'] > product.stock:
            raise serializers.ValidationError('There\'s not enough product stock')
        
        return super().validate(attrs)