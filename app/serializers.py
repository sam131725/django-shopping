from rest_framework import serializers
from .models import Product, Category, Cart

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(source='discounted_price')
    category = serializers.CharField(source='category.name')
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'image', 'rating', 'description']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.product_image:
            if request:
                return request.build_absolute_uri(obj.product_image.url)
            return obj.product_image.url
        return None

    def get_rating(self, obj):
        return 4.5  # placeholder or calculate if it exists later


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CartSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title')
    price = serializers.FloatField(source='product.discounted_price')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'title', 'price', 'quantity', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.product.product_image:
            if request:
                return request.build_absolute_uri(obj.product.product_image.url)
            return obj.product.product_image.url
        return None
