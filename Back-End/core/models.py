from django.db import models
from django.contrib.auth.models import AbstractUser
from persiantools.jdatetime import JalaliDate
from .validators import validate_phone_number


class User(AbstractUser):
    """
    Add extra fields to the default built-in django AbstractUser class
    and also has the default django permission for the User model

    username, password and email fields are required in the current implementation.
    """

    GENDER_CHOICES = [
        ('مرد', 'مرد'),
        ('زن', 'زن'),
    ]

    LANGUAGE_CHOICES = [
        ('فارسی', 'فارسی'),
        ('انگلیسی', 'انگلیسی'),
    ]

    first_name = models.CharField(max_length=25, verbose_name='نام', blank=True)
    last_name = models.CharField(max_length=30, verbose_name='نام خانوادگی', blank=True)
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    phone = models.CharField(
        max_length=11,
        validators=[validate_phone_number],
        unique=True,
        verbose_name='شماره تلفن'
    )
    image = models.ImageField(upload_to='core/images', verbose_name='تصویر', null=True, blank=True)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, verbose_name='جنسیت', null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, verbose_name='زبان', null=True, blank=True)
    date_joined = models.DateTimeField('تاریخ عضویت', auto_now_add=True)
    is_active = models.BooleanField('فعال', default=True)
    is_staff = models.BooleanField('پرسنل', default=False)
    is_superuser = models.BooleanField('ادمین', default=False)


    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = ("کاربر")
        verbose_name_plural = ("کاربرها")

    def get_joined_persian_time(self):
        return JalaliDate(self.date_joined, locale=('fa')).strftime('%c')

    get_joined_persian_time.title = 'تاریخ ثبت نام'    

    def __str__(self):
        return self.username