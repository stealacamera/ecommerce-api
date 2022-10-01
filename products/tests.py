from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from . import models


class CategoryTestCase(APITestCase):
    def setUp(self):
        admin = User.objects.create_superuser(username='admin', password='password')
        user = User.objects.create_user(username='user', password='password')
        
        data = {'username': admin.username,
                'password': 'password'}
        self.access_token = self.client.post(reverse('login'), data, format='json').data['access']
        
        data = {'username': user.username,
                'password': 'password'}
        self.user_access_token = self.client.post(reverse('login'), data, format='json').data['access']
        
        self.category = models.Category.objects.create(name='Category')
    
    def test_create_anon(self):
        data = {'name': 'New category'}
        
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_updatedelete_anon(self):
        data = {'name': 'Updated'}
        
        response = self.client.patch(reverse('category-detail', args=(self.category.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(reverse('category-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listretrieve_anon(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('category-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.user_access_token))
        
        data = {'name': 'New category'}
        
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_updatedelete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.user_access_token))
        
        data = {'name': 'Updated'}
        
        response = self.client.patch(reverse('category-detail', args=(self.category.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.delete(reverse('category-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        data = {'name': 'New category'}
        
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_updatedelete_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        data = {'name': 'Changed'}
        
        response = self.client.patch(reverse('category-detail', args=(self.category.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('category-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ProductTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='password')
        
        data = {'username': user.username,
                'password': 'password'}
        self.access_token = self.client.post(reverse('login'), data, format='json').data['access']
        
        self.category = models.Category.objects.create(name='Category')
        self.product = models.Product.objects.create(name='Product', price='10.2', stock=0)
        self.user_product = models.Product.objects.create(name='User product', price='10.2', 
                                                          stock=1, seller=user)
    
    def test_create_anon(self):
        data = {'name': 'New product',
                'description': 'Product description',
                'price': '10.2',
                'stock': 100,
                'categories': [self.category]}
        
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_updatedelete_anon(self):
        data = {'name': 'Changed'}
        
        response = self.client.patch(reverse('product-detail', args=(self.product.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.delete(reverse('product-detail', args=(self.product.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listretrieve_anon(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('product-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        data = {'name': 'New product',
                'description': 'Product description',
                'price': '10.2',
                'stock': 100,
                'categories': [self.category]}
        
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_updatedelete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        data = {'name': 'Changed'}
        
        # testing for user-created product
        
        response = self.client.patch(reverse('product-detail', args=(self.user_product.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('product-detail', args=(self.user_product.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # testing for non-user-create product
        
        response = self.client.patch(reverse('product-detail', args=(self.product.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.delete(reverse('product-detail', args=(self.product.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ReviewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='password')
        user2 = User.objects.create_user(username='user2', password='password')
        
        data = {'username': user.username,
                'password': 'password'}
        self.access_token = self.client.post(reverse('login'), data, format='json').data['access']
        
        self.product = models.Product.objects.create(name='Product', price='10.2',
                                                     stock=1, seller=user2)
        self.product2 = models.Product.objects.create(name='Product2', price='10.2',
                                                     stock=1, seller=user2)
        self.user_product = models.Product.objects.create(name='User product', price='10.2', 
                                                          stock=1, seller=user)
        
        self.review = models.Review.objects.create(title='Review', rating=1, 
                                                   product=self.user_product, user=user2)
        self.user_review = models.Review.objects.create(title='User review', rating=1, 
                                                        product=self.product2, user=user)
    
    def test_create_anon(self):
        data = {'title': 'New review',
                'text': 'description',
                'rating': 1}
        
        response = self.client.post(reverse('review-list', kwargs={'product_pk':self.product.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listretrieve_anon(self):
        response = self.client.get(reverse('review-list', kwargs={'product_pk':self.product2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('review-detail', kwargs={'product_pk':self.product2.id,
                                                                    'pk':self.user_review.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))
        
        data = {'title': 'New review',
                'text': 'description',
                'rating': 1}
        
        # testing for user-created product
        
        response = self.client.post(reverse('review-list', kwargs={'product_pk':self.user_product.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # testing for non-user-created product
        
        response = self.client.post(reverse('review-list', kwargs={'product_pk':self.product.id}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # testing for multiple reviews on a single product
        
        response = self.client.post(reverse('review-list', kwargs={'product_pk':self.product.id}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_updatedelete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.access_token))

        data = {'title': 'Changed'}
        
        # testing for user-created review
        
        response = self.client.patch(reverse('review-detail', kwargs={'product_pk':self.product2.id, 
                                                                      'pk':self.user_review.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(reverse('review-detail', kwargs={'product_pk':self.product2.id,
                                                                       'pk':self.user_review.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # testing for non-user-created review
        
        response = self.client.patch(reverse('review-detail', kwargs={'product_pk':self.user_product.id, 
                                                                      'pk':self.review.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.delete(reverse('review-detail', kwargs={'product_pk':self.user_product.id, 
                                                                       'pk':self.review.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)