from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED

from .models import Order
from .serializers import CheckoutSerializer, OrderSerializer, SalesSerializer
from .paginations import OrderPagination


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serialized = CheckoutSerializer(context = {'request': request})
        serialized.save()
        
        return Response('Order placed successfully', HTTP_201_CREATED)


class SalesDisplay(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = SalesSerializer
    
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        return Order.objects.filter(product__seller=self.request.user).order_by('-date_ordered')


class OrderHistoryDisplay(ListAPIView):
    serializer_class = OrderSerializer
    
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-date_ordered')