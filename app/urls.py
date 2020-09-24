from django.urls import path

from .views import (ProductList, sales_factura_report,
                    sales_sin_factura_report, sales_vendor_report,
                    total_sales_product_report, total_sales_report, print_invoice,
                    viewsale)

from .views import CustomerList, CustomerDetail

app_name = 'app'

urlpatterns = [
    path('reports/sales/factura/', sales_factura_report, name='sales_factura'),
    path('reports/sales/no-factura/', sales_sin_factura_report, name='sales_sin_factura'),
    path('reports/sales/totals/', total_sales_report, name='sales_total'),
    path('reports/sales/products/', total_sales_product_report, name='sales_products_total'),
    path('reports/sales/vendor/<str:vendor>/', sales_vendor_report, name='sales_vendor'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('pdfs/sale/<int:sale_id>/', print_invoice, name='pdf_test'),
    path('sale/', viewsale, name='view_sale'),
    path('api/customers/', CustomerList.as_view(), name='customer-list'),
    path('api/customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
]
