from rest_framework.permissions import BasePermission
from .models import Product


operation_list = ['create', 'update', 'partial_update', 'destroy']

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in operation_list:
            return request.user.is_superuser
        
        return True

class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in operation_list:
            return request.user.is_authenticated
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.action in operation_list:
            return obj.seller == request.user
        
        return True

class IsNotSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        product = Product.objects.get(id=view.kwargs.get('product_pk'))
        
        if view.action in operation_list:
            return request.user.is_authenticated and product.seller != request.user
        
        return True
    
    def has_object_permission(self, request, view, obj):        
        if view.action in operation_list:
            return obj.user == request.user
        
        return True