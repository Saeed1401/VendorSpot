# Generated by Django 4.1.7 on 2023-07-29 15:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_alter_customer_options_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
