from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Partner(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('ruc', 'RUC'),
        ('dni', 'DNI'),
        ('ce', 'Cedula Extranjera'),
    )
    PARTNER_TYPE_CHOICES = (
        ('client', 'Cliente'),
        ('provider', 'Proveedor'),
        ('cp', 'Cliente y Proveedor'),
    )
    name = models.CharField(max_length=250)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE_CHOICES, default='client')
    document_type = models.CharField(max_length=20,choices=DOCUMENT_TYPE_CHOICES, default='ruc')
    document_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('almacenable', 'Almacenable'),
        ('servicio', 'Servicio'),
        ('consumible', 'Consumible'),
    )
    name = models.CharField(max_length=100)
    could_be_sold = models.BooleanField()
    could_be_bought = models.BooleanField()
    is_manufactured = models.BooleanField()
    product_type = models.CharField(max_length=30,choices=PRODUCT_TYPE_CHOICES, default='almacenable')
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    cost = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    stock = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
    
    def terminado_o_insumo(self):
        if self.could_be_sold and self.is_manufactured:
            return 'Terminado'
        elif self.could_be_bought:
            return 'Insumo'
        else:
            return self.product_type
 
class MaterialList(models.Model):
     product = models.ForeignKey('Product', on_delete=models.CASCADE, limit_choices_to={'is_manufactured': True})
     quantity_of_products = models.PositiveSmallIntegerField()

     def __str__(self):
        return self.product.name
     
class Component(models.Model):
    material_list = models.ForeignKey('MaterialList', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Document(models.Model):
    name = models.CharField(max_length=8)
    abbreviation = models.CharField(max_length=3)
    serial = models.CharField(max_length=3)
    current_number = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class Purchase(models.Model):
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
    document_number = models.CharField(max_length=15)
    document_type = models.ForeignKey('Document', on_delete=models.PROTECT)
    provider = models.ForeignKey('Partner', on_delete=models.PROTECT, limit_choices_to={'partner_type': 'provider'})
    date = models.DateField()
    currency = models.CharField(max_length=7, choices=CURRENCY_CHOICES, default='pen')
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    igv = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    paid_with = models.CharField(max_length=10, choices=PAID_WITH_CHOICES, default='banco')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrador')

    def __str__(self):
        return self.document_type.abbreviation + self.document_number

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey('Purchase', on_delete=models.PROTECT, related_name='purchase_details')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, limit_choices_to={'could_be_bought': True})
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=1.00)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, default=1.00)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

class Inventory(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('produccion', 'Producción'),
        ('disminucion', 'Disminución por producción'),
        ('devolucion', 'Devolución'),
        ('ingreso_interno', 'Ingreso Interno'),
    )
    date = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    document = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=1.00)

    def save(self, *args, **kwargs):
        product = Product.objects.get(pk=self.product.id)
        if self.movement_type == 'compra' or self.movement_type == 'produccion' or self.movement_type == 'devolucion' or self.movement_type == 'ingreso_interno':
            product.stock += self.quantity
        else: 
            product.stock -= self.quantity
        product.save()
        super(Inventory, self).save(*args, **kwargs)

