from django.contrib import admin
from . import models



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
    'title', 
    'slug', 
    'price', 
    'product_image', 
    'description', 
    'inventory', 
    'last_update', 
    'category'
]
    list_per_page = 10



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail']
    list_display_links = ['thumbnail']
    list_editable = ['title']
    list_per_page = 10



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date']
    list_per_page = 10