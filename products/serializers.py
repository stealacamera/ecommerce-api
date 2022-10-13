from django.db.models import Avg, IntegerField
from rest_framework import serializers

from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'num_of_products']
    
    def get_num_of_products(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source='seller.username', read_only=True)
    categories = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                              many=True, slug_field='name')
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'categories': {'required': True},
                        'price': {'required': True},
                        'stock': {'required': True}}
    
    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating', 
                                         output_field=IntegerField()))['rating__avg'] or 0

class MiniProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'text': {'required': False},
                        'rating': {'required': True}}


class ReviewRelationSerializer(ReviewSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'rating']

class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewRelationSerializer(many=True, read_only=True)