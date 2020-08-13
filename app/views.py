from django.views.generic import ListView
from .models import Product


class ProductList(ListView):
    #model = Product
    queryset = Product.productos.all()
    context_object_name = 'products'
    paginate_by = 20