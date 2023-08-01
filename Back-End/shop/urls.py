from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('customers', views.CustomerViewSet)
router.register('carts', views.CartViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
