# Generated by Django 4.1.7 on 2023-07-29 14:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shop.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('slug', models.SlugField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(10000)], verbose_name='ریال)قیمت)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='shop/images', validators=[shop.validators.file_size_validation], verbose_name='عکس کالا')),
                ('inventory', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='موجود در انبار')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='اخرین بروزرسانی')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالاها',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(validators=[shop.validators.validate_phone_number], verbose_name='شماره تلفن')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
    ]
