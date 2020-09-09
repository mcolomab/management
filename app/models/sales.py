from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .documents import Document
from .inventories import Inventory
from .partners import Partner
from .products import Product

PAID_WITH_CHOICES = (
    ('banco', 'Banco'),
    ('efectivo', 'Efectivo'),
)
STATUS_CHOICES = (
    ('borrador', 'Borrador'),
    ('confirmada', 'Confirmada'),
    ('despachada', 'Despachada'),
    ('pagada', 'Pagada'),
    ('anulada', 'Anulada'),
)
CURRENCY_CHOICES = (
    ('pen', 'Soles'),
)
VENDOR_CHOICES = (
    ('oficina', 'Oficina'),
    ('lady', 'Lady'),
    ('sugey', 'Sugey'),
    ('aracelli', 'Aracelli'),
    ('jasmina', 'Jasmina'),
)

class Sale(models.Model):
    document_number = models.CharField(max_length=15)
    document_type = models.ForeignKey(Document, on_delete=models.PROTECT)
    customer = models.ForeignKey(Partner, on_delete=models.PROTECT, limit_choices_to={'partner_type': 'customer'})
    sale_date = models.DateField()
    expiration_date = models.DateField()
    vendor = models.CharField(max_length=10, choices=VENDOR_CHOICES, default='oficina')
    currency = models.CharField(max_length=7, choices=CURRENCY_CHOICES, default='pen')
    sub_total = models.FloatField(default=0)
    igv = models.FloatField(default=0)
    total = models.FloatField(default=0)
    amount_paid = models.FloatField(default=0)
    paid_with = models.CharField(max_length=10, choices=PAID_WITH_CHOICES, default='efectivo')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrador')

    def __str__(self):
        return self.document_type.abbreviation + self.document_number
    
    def save(self, *args, **kwargs):
        if self.id and self.status == 'anulada':
            for item in Inventory.objects.filter(document__icontains=self.document_number):
                item.delete()
        
        if not self.id:
            doc = Document.objects.get(id=self.document_type.id)
            self.document_number = doc.serial + '-' + str(doc.current_number)
            doc.current_number += 1
            doc.save()

        if self.status == 'confirmada':
            for item in SaleDetail.objects.filter(sale=self.id):
                Inventory.objects.create(
                    movement_type='venta',
                    product=item.product,
                    quantity=item.quantity,
                    document=self.document_type.abbreviation+self.document_number
                )
            self.status = 'despachada'

        anulada = True if self.status == 'anulada' else False
        
        if self.amount_paid > 0 and not anulada and self.amount_paid == self.total:
            self.status = 'pagada'
        
        super(Sale, self).save(*args, **kwargs)

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='sale_details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, limit_choices_to={'could_be_sold': True})
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField(default=1)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def save(self, *args, **kwargs):
        sale = Sale.objects.get(pk=self.sale.id)
        if sale.document_type.abbreviation.lower() == 'fac':
            sub_total = self.quantity * self.unit_price * 1 - self.discount/100
            igv = self.quantity * self.unit_price * 0.18
        elif sale.document_type.abbreviation.lower() == 'bol':
            sub_total = self.quantity * self.unit_price * 0.18 * 1 - self.discount/100
            igv = 0
        else:
            sub_total = self.quantity * self.unit_price * 1 - self.discount/100
            igv = 0

        sale.sub_total += sub_total
        sale.igv += igv
        sale.total += sub_total + igv
        sale.save()
        super(SaleDetail, self).save(*args, **kwargs)

    def delete(self):
        sale = Sale.objects.get(pk=self.sale.id)
        if sale.document_type.abbreviation.lower() == 'fac':
            sub_total = self.quantity * self.unit_price * 1 - self.discount/100
            igv = self.quantity * self.unit_price * 0.18
        elif sale.document_type.abbreviation.lower() == 'bol':
            sub_total = self.quantity * self.unit_price * 0.18 * 1 - self.discount/100
            igv = 0
        else:
            sub_total = self.quantity * self.unit_price * 1 - self.discount/100
            igv = 0

        sale.sub_total -= sub_total
        sale.igv -= igv
        sale.total -= sub_total + igv
        sale.save()

        super(SaleDetail, self).delete()
