from django.views.generic import ListView

from app.models import Product


class ProductList(ListView):
    #model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 20
