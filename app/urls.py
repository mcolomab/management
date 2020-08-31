from django.urls import path

from .views import (ProductList, sales_factura_report,
                    sales_sin_factura_report, sales_vendor_report,
                    total_sales_product_report, total_sales_report)

app_name = 'app'

urlpatterns = [
    path('reports/sales/factura/', sales_factura_report, name='sales_factura'),
    path('reports/sales/no-factura/', sales_sin_factura_report, name='sales_sin_factura'),
    path('reports/sales/totals/', total_sales_report, name='sales_total'),
    path('reports/sales/products/', total_sales_product_report, name='sales_products_total'),
    path('reports/sales/vendor/<str:vendor>/', sales_vendor_report, name='sales_vendor'),
    path('products/', ProductList.as_view(), name='product_list'),
]
