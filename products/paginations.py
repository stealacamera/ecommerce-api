from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 50


class ReviewPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20