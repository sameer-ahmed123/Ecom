# Generated by Django 5.1.5 on 2025-02-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_product_brand_product_detailed_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='filesize',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='format',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='variant_description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='file',
            field=models.FileField(blank=True, help_text='Only required if variant is Digital', null=True, upload_to='digital_files/'),
        ),
    ]
