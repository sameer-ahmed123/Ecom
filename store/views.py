from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


def index(request):
    return render(request, "index.html")


def product_list_view(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {"product": product})


def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect("product_list")
        else:
            form.add_error(None, "You must be logged in to add a product.")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})


def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
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
