from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.CartDisplay, basename='cart')

urlpatterns = [
    path('add/<int:product_pk>/', views.CreateCartView.as_view(), name='add-to-cart'),
    path('', include(router.urls)),
]