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
    
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'categories': {'required': True},
                        'price': {'required': True},
                        'stock': {'required': True},
                        'rating': {'read_only': True}}


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'text': {'required': False},
                        'rating': {'required': True}}
    
    def save(self, **kwargs):
        if self.context['request'].method == 'POST':
            product = Product.objects.get(id=self.context['product_pk'])
            review_rating = self.validated_data['rating']
            
            if Review.objects.filter(user=self.context['request'].user, product=product).exists():
                raise serializers.ValidationError('You have already reviewed this product')
            
            if product.rating == 0:
                product.rating = review_rating
            else:
                product.rating = (product.rating + review_rating) / 2
            
            product.save()
        return super().save(**kwargs)


class ReviewRelationSerializer(ReviewSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'rating']

class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewRelationSerializer(many=True, read_only=True)