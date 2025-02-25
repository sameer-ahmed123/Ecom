# Generated by Django 5.1.5 on 2025-02-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_product_price_product_base_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0, help_text='Stock quantity for products without variants'),
        ),
    ]
