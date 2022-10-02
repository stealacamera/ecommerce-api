from rest_framework.pagination import LimitOffsetPagination

class OrderPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50