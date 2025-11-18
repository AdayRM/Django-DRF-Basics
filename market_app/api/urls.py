
from django.urls import path
from .views import markets_view, sellers_view, single_market_view, products_view, single_product_view, single_seller_view

urlpatterns = [
    path('markets/', markets_view),
    path('markets/<int:pk>/', single_market_view, name="market-detail"),
    path('sellers/', sellers_view),
    path('sellers/<int:pk>/', single_seller_view, name="seller-detail"),
    path('products/', products_view),
    path('products/<int:pk>/', single_product_view, name="product-detail"),


]
