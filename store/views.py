from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Product, ProductVariant
from .forms import ProductForm, ProductVariantFormset, ProductVariantForm,ProductVariantInlineFormSet
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

def index(request):
    return render(request, "index.html")

def product_list_view(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {"product": product})

def get_formset_class(product_type):
    Formset = inlineformset_factory(
        Product,
        ProductVariant,
        form=ProductVariantForm,
        formset=ProductVariantInlineFormSet,
        extra=1,
        can_delete=True
    )
    # Attach product_type to the formset class so it is passed on form instantiation.
    Formset.product_type = product_type
    return Formset


@login_required
def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        product_type = request.POST.get('product_type', 'physical')
        Formset = get_formset_class(product_type)
        formset = Formset(request.POST, request.FILES, prefix='variants')
        if request.user.is_authenticated:
            if form.is_valid() and formset.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                form.save_m2m()

                # Save variants if any
                variants = formset.save(commit=False)
                for variant in variants:
                    variant.product = product
                    # For digital variants, force stock_quantity to 1
                    if product_type == "digital":
                        variant.stock_quantity = 1
                    variant.save()

                if not variants and product.stock_quantity <= 0:
                    form.add_error(
                        'stock_quantity',
                        "Stock quantity is required for products without variants"
                    )
                    return render(request, "product_form.html", {
                        "form": form,
                        "formset": formset
                    })
                return redirect("product_detail", slug=product.slug)
        else:
            form.add_error(None, "You must be logged in to add a product.")
    else:
        form = ProductForm()
        formset = ProductVariantFormset(prefix='variants')
    context = {
        "form": form,
        "formset": formset
    }
    return render(request, "product_form.html", context)

@login_required
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, "product_form.html", {"form": form})

def product_delete_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "product_confirm_delete.html", {"product": product})
