from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    categories = models.ManyToManyField(Category, related_name='products')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    
    def __str__(self):
        return self.name


def get_deleted_user():
    return User.objects.get_or_create(username='deactivated')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=70)
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=(MinValueValidator(1), MaxValueValidator(5),))

    def __str__(self):
        return self.user.username + ': ' + self.title