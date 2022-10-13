from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Category, Product, Review
from . import serializers, permissions
from .paginations import CustomPagination, ReviewPagination
from orders.models import Order


class CategoryDisplay(ModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
    permission_classes = [permissions.IsAdminOrReadOnly]


class ProductDisplay(ModelViewSet):
    queryset = Product.objects.all()
    
    permission_classes = [permissions.IsSellerOrReadOnly]
    pagination_class = CustomPagination
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['categories']
    ordering_fields = ['price']
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        
        return serializers.ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    def perform_destroy(self, instance):
        if Order.objects.filter(product=instance, status='Ordered').exists():
            raise ValidationError('A product with orders cannot be deleted')
        
        instance.delete()


class ReviewDisplay(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    
    permission_classes = [permissions.IsNotSellerOrReadOnly]
    pagination_class = ReviewPagination
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']
    
    def get_queryset(self):
        pk = self.kwargs['product_pk']
        return Review.objects.filter(product__id=pk)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'product_pk': self.kwargs['product_pk']})
        return context
    
    def perform_create(self, serializer):
        product = Product.objects.get(id=self.kwargs['product_pk'])
        serializer.save(user=self.request.user, product=product)
