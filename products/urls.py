from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


review_router = DefaultRouter()
review_router.register('reviews', views.ReviewDisplay, basename='review')

router = DefaultRouter()
router.register('category', views.CategoryDisplay, basename='category')
router.register('', views.ProductDisplay, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:product_pk>/', include(review_router.urls)),
]
