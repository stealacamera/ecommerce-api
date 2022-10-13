from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    country = models.CharField(max_length=90)
    city = models.CharField(max_length=80)
    street_address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=16)
    
    def __str__(self):
        return self.user.username + " address"