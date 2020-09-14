import io

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from app.models import Sale, SaleDetail
from django.http import FileResponse

from app.helpers import formatFloats, formarQuantity, numberToStr, FACTURA

def drawInvoice(p, sale_id):
    # Configuracion de la letra (tipografia, alto)
    p.setFont("Helvetica", 8)

    sale = Sale.objects.get(id=sale_id)

    # Dibujo de la cabecera
    p.drawString(3.3*cm, 16.5*cm, sale.customer.name)
    p.drawString(3.3*cm, 15.8*cm, sale.customer.address)
    p.drawString(10.7*cm, 15.1*cm, sale.customer.document_number)
    p.drawString(16.3*cm, 15.1*cm, sale.sale_date.strftime("%d/%m/%Y"))

    # Dibujo del detalle de la factura
    base_alta = 13.6*cm
    cantidad = 2.5*cm
    descripcion = 4.3*cm
    pu = 15.3*cm
    importe = 18*cm

    for item in SaleDetail.objects.filter(sale=sale_id):
        p.drawString(cantidad, base_alta, formarQuantity(item.quantity))
        p.drawString(descripcion, base_alta, item.product.name)
        p.drawString(pu, base_alta, formatFloats(item.unit_price))
        p.drawString(importe, base_alta, formatFloats(item.quantity * item.unit_price))
        base_alta -= .5*cm

    # Dibujar resumen de factura
    p.drawString(3*cm, 3.9*cm, numberToStr(sale.total))
    p.drawString(importe, 3.1*cm, formatFloats(sale.sub_total))
    p.drawString(16.3*cm, 2.4*cm, "18")
    p.drawString(importe, 2.4*cm, formatFloats(sale.igv))
    p.drawString(importe, 1.7*cm, formatFloats(sale.total))

def print_invoice(request, sale_id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=FACTURA)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    drawInvoice(p, sale_id)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
