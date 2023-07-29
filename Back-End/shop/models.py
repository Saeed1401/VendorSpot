from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from persiantools.jdatetime import JalaliDate
from uuid import uuid4
from .validators import file_size_validation, validate_phone_number


# custom User model
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=70, verbose_name='عنوان')
    thumbnail = models.ImageField(
        upload_to='shop/images', 
        verbose_name='تصویر دسته'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = ("دسته بندی")
        verbose_name_plural = ("دسته بندی ها")
        ordering = ["title"]



class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField()
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        verbose_name='ریال)قیمت)',
        validators=[
            MinValueValidator(10000),
        ],
    )
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    product_image = models.ImageField(
        upload_to='shop/images', 
        validators=[file_size_validation],
        verbose_name='عکس کالا',
        null=True,
        blank=True
        )
    inventory = models.IntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name='موجود در انبار'
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name='اخرین بروزرسانی'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='products'
    )

    def get_jalali_last_update(self):
        return JalaliDate(self.last_update, locale=('fa')).isoformat()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = ('کالا')
        verbose_name_plural = ('کالاها')
        ordering = ['title']



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(
        validators=[validate_phone_number], 
        verbose_name='شماره تلفن'
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name = ("مشتری")
        verbose_name_plural = ("مشتری ها")
        ordering = ['user__first_name', 'user__last_name']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("کارت")
        verbose_name_plural = ("کارت ها")


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name='مقدار'
    )

    class Meta:
        verbose_name = ("ایتم")
        verbose_name_plural = ("ایتم ها")
        unique_together = [
            ['cart', 'product'], # to prevent duplicates in cart
        ]


