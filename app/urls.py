from django.urls import path
from .views import ProductList


app_name = 'app'

urlpatterns = [
    path('products', ProductList.as_view(), name='product_list'),
]