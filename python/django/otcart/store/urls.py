from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products-list'),
    path('products/detail/<slug:productid>', views.ProductDetailView.as_view(), name='product-detail'),
]