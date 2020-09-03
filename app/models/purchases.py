from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    ('recibida', 'Recibida'),
    ('pagada', 'Pagada'),
)
CURRENCY_CHOICES = (
    ('pen', 'Soles'),
    ('usd', 'Dólares'),
)
DOCUMENT_TYPES = (
    ('factura', 'Factura'),
    ('boleta', 'Boleta'),
    ('proforma', 'Proforma'),
)

class Purchase(models.Model):
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, default='factura')
    document_number = models.CharField(max_length=15)
    provider = models.ForeignKey(Partner, on_delete=models.PROTECT, limit_choices_to={'partner_type': 'provider'})
    purchase_date = models.DateField()
    expiration_date = models.DateField()
    currency = models.CharField(max_length=7, choices=CURRENCY_CHOICES, default='pen')
    sub_total = models.FloatField()
    igv = models.FloatField()
    total = models.FloatField()
    amount_paid = models.FloatField(default=0)
    paid_with = models.CharField(max_length=10, choices=PAID_WITH_CHOICES, default='banco')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrador')

    def __str__(self):
        return self.document_type.upper()[:3] + self.document_number

    def save(self, *args, **kwargs):
        if self.status == 'confirmada':
            for item in PurchaseDetail.objects.filter(purchase=self.id):
                Inventory.objects.create(
                    movement_type='compra',
                    product=item.product,
                    quantity=item.quantity,
                    document=self.document_type.upper()[:3]+self.document_number
                )
            if PurchaseDetail.objects.filter(purchase=self.id):
                self.status = 'recibida'

        if self.amount_paid > 0 and self.amount_paid == self.total:
            self.status = 'pagada'
        
        super(Purchase, self).save(*args, **kwargs)

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='purchase_details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, limit_choices_to={'could_be_bought': True})
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField(default=1)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
