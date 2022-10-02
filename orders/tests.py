from itertools import product
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Order
from products.models import Product
from cart.models import CartItem


class CheckoutTestCase(APITestCase):
    def setUp(self) :
        user = User.objects.create_user(username='user', password='password')
        user2 = User.objects.create_user(username='user2', password='password')
        
        data = {'username': user.username,
                'password': 'password'}
        access_token = self.client.post(reverse('login'), data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        
        self.product = Product.objects.create(name='Product', seller=user2, price='10.2', stock=4)
        self.cart = CartItem.objects.create(user=user, product=self.product, quantity=1)
    
    def test_checkout(self):
        response = self.client.post(reverse('checkout'))
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='password')
        user2 = User.objects.create_user(username='user2', password='password')
        
        data = {'username': user.username,
                'password': 'password'}
        access_token = self.client.post(reverse('login'), data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        
        self.product = Product.objects.create(name='Product', price='10.2', stock=4)
        self.user_product = Product.objects.create(name='User product', price='10.2', stock=4)
        
        self.order = Order.objects.create(seller=user2, customer=user, product=self.product, quantity=1)
        self.sale = Order.objects.create(seller=user, customer=user2, product=self.product, quantity=1)
    
    def test_get_orders(self):
        response = self.client.get(reverse('products-ordered'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getretrieve_sales(self):
        response = self.client.get(reverse('sales-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('sales-detail', args=(self.sale.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatedelete_sales(self):
        data = {'status': 'Refunded'}
        
        response = self.client.delete(reverse('sales-detail', args=(self.sale.id,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.put(reverse('sales-detail', args=(self.sale.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('sales-detail', args=(self.sale.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)