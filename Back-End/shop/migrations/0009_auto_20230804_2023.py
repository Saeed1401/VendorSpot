# Generated by Django 4.2.3 on 2023-08-04 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_orderitem_product'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE shop_customer DROP COLUMN phone;")
    ]
