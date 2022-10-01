from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CheckoutView, SalesDisplay, OrderHistoryDisplay


router = DefaultRouter()
router.register('sales', SalesDisplay, basename='sales')

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('history/', OrderHistoryDisplay.as_view(), name='products-ordered'),
    path('', include(router.urls)),
]