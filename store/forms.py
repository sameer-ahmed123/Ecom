from django.forms.models import BaseInlineFormSet
from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductVariant, Tag, ProductReview, Category


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        # Always include the file field in the base fields.
        fields = ['price', 'variant_type', 'variant_description',
                  'stock_quantity', 'file', 'variant_image']

    def __init__(self, *args, **kwargs):
        # Pop product_type if provided; default to 'physical' if not.
        product_type = kwargs.pop('product_type', None)
        if product_type is None:
            product_type = 'physical'
        super().__init__(*args, **kwargs)

        # Ensure the file field is always present.
        if 'file' not in self.fields:
            self.fields['file'] = forms.FileField(required=False)
        if 'variant_image' not in self.fields:
            self.fields['variant_image'] = forms.ImageField(required=False)

        if product_type == 'physical':
            # For physical variants, add physical-specific fields with widget classes.
            self.fields.update({
                'size': forms.CharField(
                    required=False,
                    widget=forms.TextInput(attrs={"class": "physical-fields"})
                ),
                'color': forms.CharField(
                    required=False,
                    widget=forms.TextInput(attrs={"class": "physical-fields"})
                ),
                'weight': forms.DecimalField(
                    required=False,
                    widget=forms.NumberInput(
                        attrs={"class": "physical-fields"})
                ),
                'dimensions': forms.CharField(
                    required=False,
                    widget=forms.TextInput(attrs={"class": "physical-fields"})
                ),
                # Ensure stock_quantity is required for physical variants.
                'stock_quantity': forms.IntegerField(
                    required=True,
                    widget=forms.NumberInput(
                        attrs={"class": "physical-fields"})
                ),
            })
            # Not required for physical variants.
            self.fields['file'].required = False
        else:
            # For digital variants, require the file and add a CSS class for later toggling.
            self.fields['file'].required = True
            # self.fields['variant_image'].required = True
            self.fields['file'].widget = forms.ClearableFileInput(
                attrs={"class": "digital-fields"})
            # self.fields['variant_image'] = forms.ClearableFileInput(
            #     attrs={"class": "digital-fields"})
            # Hide stock_quantity for digital variants.
            self.fields['stock_quantity'].widget = forms.HiddenInput()


class ProductVariantInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        # Pass product_type from the formset instance to each form;
        # default to 'physical' if not set.
        kwargs['product_type'] = getattr(self, 'product_type', 'physical')
        return super()._construct_form(i, **kwargs)


# Use our custom formset in the inlineformset_factory.
ProductVariantFormset = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    formset=ProductVariantInlineFormSet,
    extra=1,
    can_delete=True
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'tags': forms.SelectMultiple(attrs={"class": "select2"}),
            'category': forms.Select(attrs={"class": "form-control"})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_type', 'name', 'brand', 'main_image', 'digital_file',
            'description', 'detailed_description', 'features', 'base_price', 'sale_price',
            'category', 'tags', 'stock_quantity'
        ]
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'help_text': 'Only required for products without variants'
            }),
            # Additional widgets can be added here as needed.
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = "__all__"
