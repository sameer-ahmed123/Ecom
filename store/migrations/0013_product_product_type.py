# Generated by Django 5.1.5 on 2025-02-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_productvariant_filesize_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('physical', 'Physical Product'), ('digital', 'Digital Product')], default='physical', max_length=10),
        ),
    ]
