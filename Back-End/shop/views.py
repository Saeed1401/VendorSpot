from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import (Product,
    Category,
    Customer,
    OrderItem
)
from .serializers import (ProductSerializer,
    CategorySerializer,
    CustomerSerializer
)


# custom User model
User = get_user_model()


class ProductViewSet(ModelViewSet):
    """
    list and create operation for Product
    as well as get, update and delete a particular Product
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
            return Response(
                {'error': 'You cannot delete this product, because it\'s associated with an orderitem'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


    
class CategoryViewSet(ModelViewSet):
    """
    list and create operation for Category
    as well as get, update and delete a particular Category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(category_id=self.kwargs['pk']).count() > 0:
            return Response(
                {'error': 'You cannot delete this category, because it\'s category contanis one or more products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)
    

    
class CustomerViewSet(ModelViewSet):
    """
    List and create operation for Customer
    as well as get, update and delete a particular Customer
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

