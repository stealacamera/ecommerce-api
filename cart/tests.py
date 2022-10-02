from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import CartItem
from products.models import Product


class CartTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='password')
        
        data = {'username': user.username,
                'password': 'password'}
        access_token = self.client.post(reverse('login'), data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        
        self.product1 = Product.objects.create(name='Product', price='10.2', stock=4)
        self.product2 = Product.objects.create(name='Product 2', price='10.2', stock=4)
        self.user_product = Product.objects.create(name='User product', price='10.2', 
                                                   stock=4, seller=user)
        
        self.cart = CartItem.objects.create(user=user, product=self.product2, quantity=1)
    
    def test_addtocart(self):
        data = {'quantity': 2}
        
        # Testing for non-user product
        response = self.client.post(reverse('add-to-cart', kwargs={'product_pk': self.product1.id}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Testing for user product
        response = self.client.post(reverse('add-to-cart', kwargs={'product_pk': self.user_product.id}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_getretrieve(self):
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('cart-detail', args=(self.cart.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatedelete(self):
        data = {'quantity': 2}
        
        response = self.client.put(reverse('cart-detail', args=(self.cart.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('cart-detail', args=(self.cart.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)