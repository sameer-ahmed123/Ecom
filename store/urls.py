from django.urls import path
from .views import product_list_view, product_detail_view, product_create_view, product_update_view, product_delete_view

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('products/', product_list_view, name='product_list'),
    path('products/new/', product_create_view, name='product_create'),
    path('products/<slug:slug>/', product_detail_view, name='product_detail'),
    path('products/<slug:slug>/edit/', product_update_view, name='product_update'),
    path('products/<int:id>/delete/', product_delete_view, name='product_delete'),
]