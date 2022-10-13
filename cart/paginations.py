from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response
from collections import OrderedDict


class CartPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
    
    def get_paginated_response(self, data):
        subtotal = 0
        
        for obj in data:
            subtotal += obj['total']
        
        return Response(OrderedDict([
            ('subtotal', subtotal),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))