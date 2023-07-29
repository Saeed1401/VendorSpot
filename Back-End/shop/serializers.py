from rest_framework import serializers
from django.utils.text import slugify
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    def get_slug(self, instance):
        return slugify(instance.title)

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