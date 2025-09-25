from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/products/<int:product_id>/', views.product_api, name='product_api'),
    path('api/categories/count/', views.category_products_count, name='category_count'),
]