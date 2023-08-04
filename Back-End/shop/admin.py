from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
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
    'category',
    'get_jalali_last_update'
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
    list_display = ['user', 'user_id', 'birth_date']
    list_select_related = ['user']
    list_per_page = 10

    def user_id(self, customer):
        url = (
            reverse('admin:core_user_changelist')
            + '?'
            + urlencode(
                {
                    'user__id': str(customer.user.id)
                }
            )
        )
        return format_html('<a href="{}" >{}</a>', url, customer.user.id)