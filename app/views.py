import csv

from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product, Sale, Document, SaleDetail, Partner


class ProductList(ListView):
    #model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 20

def update_lists(plist, qlist, product, quantity):
    if product not in plist:
        plist.append(product)
        qlist.append(quantity)
    else:
        i = plist.index(product)
        new_quantity = qlist[i] + quantity
        qlist.pop(i)
        qlist.insert(i, new_quantity)

def total_sales_product_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos_vendidos.csv"'

    sales = Sale.objects.filter(
        sale_date__gte='2020-08-01',
        sale_date__lte='2020-08-31'
    ).exclude(status='borrador').exclude(status='anulada').exclude(status='blanco')

    products = []
    quantities = []
    for sale in sales:
        for dt in SaleDetail.objects.filter(sale=sale):
            update_lists(products, quantities, dt.product, dt.quantity)

    writer = csv.writer(response)
    writer.writerow(['Producto', 'Cantidad'])
    for product in products:
        writer.writerow([product.name, quantities[products.index(product)]])

    return response

def total_sales_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas.csv"'

    sb = Partner.objects.get(document_number='10070823956')

    sales = Sale.objects.filter(
        sale_date__gte='2020-08-01',
        sale_date__lte='2020-08-31'
    ).exclude(status='borrador').exclude(status='anulada').exclude(status='blanco').exclude(customer=sb)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro. Documento', 'Cliente', 'Sub Total', 'Pagado'])
    for sale in sales:
        writer.writerow([sale.sale_date, sale.document_number, sale.customer.name.upper(), sale.sub_total, sale.amount_paid])

    return response

def sales_factura_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas_factura.csv"'

    doc = Document.objects.get(name='FACTURA')
    sb = Partner.objects.get(document_number='10070823956')

    sales = Sale.objects.filter(
        sale_date__gte='2020-08-01',
        sale_date__lte='2020-08-31',
        document_type_id=doc.id
    ).exclude(status='borrador').exclude(status='anulada').exclude(status='blanco').exclude(customer=sb)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro. Documento', 'Cliente', 'Sub Total', 'IGV', 'Total', 'Pagado'])
    for sale in sales:
        writer.writerow([sale.sale_date, sale.document_number, sale.customer.name.upper(), sale.sub_total, sale.igv, sale.total, sale.amount_paid])

    return response

def sales_sin_factura_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas_sin_factura.csv"'

    doc = Document.objects.get(name='FACTURA')

    sales = Sale.objects.filter(
        sale_date__gte='2020-08-01',
        sale_date__lte='2020-08-31'
    ).exclude(status='borrador').exclude(status='anulada').exclude(status='blanco').exclude(document_type_id=doc.id)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro. Documento', 'Sub Total', 'IGV', 'Total', 'Pagado'])
    for sale in sales:
        writer.writerow([sale.sale_date, sale.document_number, sale.sub_total, sale.igv, sale.total, sale.amount_paid])

    return response

def sales_vendor_report(request, vendor):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventas_'+vendor+'.csv"'

    sales = Sale.objects.filter(
        sale_date__gte='2020-08-01',
        sale_date__lte='2020-08-31',
        vendor=vendor
    ).exclude(status='borrador').exclude(status='anulada').exclude(status='blanco')
    
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro. Documento', 'Cliente', 'Sub Total', 'IGV', 'Total', 'Pagado'])
    for sale in sales:
        writer.writerow([sale.sale_date, sale.document_number, sale.customer.name.upper(), sale.sub_total, sale.igv, sale.total, sale.amount_paid])

    return response
