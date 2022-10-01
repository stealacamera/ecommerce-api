from random import choices
from django.db import models
from django.contrib.auth.models import User

from products.models import Product
from products.models import get_deleted_user


class Order(models.Model):
    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    REFUNDED = 'Refunded'
    
    ORDER_STATUS_CHOICES = [
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (REFUNDED, 'Refunded')
    ]
    
    seller = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name='placed_orders')
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default=ORDERED)