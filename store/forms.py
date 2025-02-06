from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'sale_price',
                  'stock_quantity', 'is_in_stock', 'category', 'tags']
