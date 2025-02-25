from django.contrib import admin
from .models import Product, Tag, Category, ProductReview, ProductVariant


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    @admin.display(description='URL')
    def url(self, obj):
        return obj.get_absolute_url()  # Properly calling the method

    list_display = ['name', 'base_price', 'sale_price', 'url','total_stock', 'date_added', 'date_updated']
    list_filter = ['date_added', 'date_updated']
    search_fields = ['name', 'description']



class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity','price']
    list_filter = ['product','color', 'size','price']
    search_fields = ['size', 'product__name','color']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'date_created']
    list_filter = ['date_created']
    search_fields = ['product__name', 'user__username']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Product, ProductAdmin)
