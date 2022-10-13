from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import mixins

from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from products.models import Product
from .serializers import CartItemSerializer
from .paginations import CartPagination


class CreateCartView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'product_pk': self.kwargs['product_pk']})
        return context
    
    def perform_create(self, serializer):
        pk = self.kwargs['product_pk']
        product = Product.objects.get(id=pk)
        
        serializer.save(product=product)


class CartDisplay(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = CartItemSerializer
    
    permission_classes = [IsAuthenticated]
    pagination_class = CartPagination
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)