from rest_framework import serializers
from django.utils.text import slugify
from .models import Product, Category, Customer, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()


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

    def get_slug(self, instance):
        return slugify(instance.title) # to automatically fill the slug field in product by title

    def get_product_image_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.product_image.url
        return request.build_absolute_url(photo_url)



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'thumbnail']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.thumbnail.url
        return request.build_absolute_uri(photo_url)
    

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date']


class EssentialProductFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product = EssentialProductFieldSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


    def get_total_price(self, obj):
        return sum(item.quantity * item.product.price for item in obj.items.all())