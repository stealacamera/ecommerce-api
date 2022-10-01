from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.user.username} cart: {self.product.name}'