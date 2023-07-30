from rest_framework import serializers
from django.utils.text import slugify
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    def get_slug(self, instance):
        return slugify(instance.title) # to automatically fill the slug field in product by title

    class Meta:
        model = Product
        fields = [
            'product_image', 
            'title', 
            'slug', 
            'price', 
            'description', 
            'inventory', 
            'last_update', 
            'category'
        ]



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'thumbnail']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.thumbnail.url
        return request.build_absolute_uri(photo_url)