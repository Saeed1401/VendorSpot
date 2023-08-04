from rest_framework import serializers
from django.utils.text import slugify
from django.db import transaction
from .models import Product, Category, Customer, Cart, CartItem, Order, OrderItem





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
        fields = ['id', 'user_id', 'birth_date']





class EssentialProductFieldSerializer(serializers.ModelSerializer):
    """
    Provide the basic fields of a product
    """

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']




class CartItemSerializer(serializers.ModelSerializer):
    """
    To get the items of a cart(not used for create or update)
    """

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
    




class CreateCartItemSerializer(serializers.ModelSerializer):
    """
    used to create a cart item in the /carts/(cart_id)/items/ endpoint
    """

    product_id = serializers.IntegerField()

    def validate_product_id(self, id):
        if not Product.objects.filter(pk=id).exists():
            raise serializers.ValidationError('No product with the given id was found')
        return id

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    """
    used to update the quantity of a product in a specific cartitem
    """
    class Meta:
        model = CartItem
        fields = ['quantity']



class OrderItemSerializer(serializers.ModelSerializer):
    product = EssentialProductFieldSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'ordered_at', 'customer', 'items']





class CreateOrderSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, obj):
        if not Cart.objects.filter(pk=obj).exists():
            return serializers.ValidationError('No cart with the given ID was found!!')
        if CartItem.objects.filter(cart_id=obj).count() == 0:
            return serializers.ValidationError('the given cart is empty!!')
        return obj
    
    def create(self, validated_data):

        with transaction.atomic(): # if something goes wrong the whole process would stop
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get(user_id=self.context['user_id'])
            
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=cart_items.product,
                    price=cart_items.price,
                    quantity=cart_items.quantity
                ) for item in cart_items # iterate through cartitems and create orderitem objects
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete() # delete the cart after creating the order which is associated with

            return order

    class Meta:
        model = Order
        fields = ['cart_id']