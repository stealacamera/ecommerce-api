from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {'username': 'user',
                'first_name': 'name',
                'last_name': 'surname',
                'email': 'email@example.com',
                'password': 'password',
                'password2': 'password',
                'address': {
                    'country': 'country',
                    'city': 'city',
                    'street_address': 'user address 123',
                    'zip_code': '1000'}}
        
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ChangeInfo(APITestCase):
    def setUp(self):
        data = {'username': 'user',
                'first_name': 'name',
                'last_name': 'surname',
                'email': 'email@example.com',
                'password': 'password',
                'password2': 'password',
                'address': {
                    'country': 'country',
                    'city': 'city',
                    'street_address': 'user address 123',
                    'zip_code': '1000'}}
        
        tokens = self.client.post(reverse('register'), data, format='json').data['tokens']
        self.refresh_token = tokens['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access']))
    
    def test_updateusername(self):
        data = {'new_username': 'changed'}
        
        response = self.client.put(reverse('personal-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatepassword(self):
        
        # testing for unchanged new password
        
        data = {'current_password': 'password',
                'new_password': 'password',
                'refresh': self.refresh_token}
        
        response = self.client.put(reverse('change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # testing for changed password
        
        data = {'current_password': 'password',
                'new_password': 'changed',
                'refresh': self.refresh_token}
        
        response = self.client.put(reverse('change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updatecontact(self):
        data = {'country': 'country',
                'city': 'new city',
                'street_address': 'new address 345',
                'zip_code': '1234'}
        
        response = self.client.put(reverse('change-address'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProfileTestCase(APITestCase):
    def setUp(self):
        data = {'username': 'user',
                'first_name': 'name',
                'last_name': 'surname',
                'email': 'email@example.com',
                'password': 'password',
                'password2': 'password',
                'address': {
                    'country': 'country',
                    'city': 'city',
                    'street_address': 'user address 123',
                    'zip_code': '1000'}}
        
        user_data = self.client.post(reverse('register'), data, format='json')
        self.tokens = user_data.data['tokens']
        self.username = user_data.data['username']
    
    def test_getpersonalprofile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.tokens['access']))
        
        response = self.client.get(reverse('personal-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getprofile(self):
        response = self.client.get(reverse('user-profile', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)