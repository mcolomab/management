from django.db import models

from .products import Product


MOVEMENT_TYPE_CHOICES = (
    ('compra', 'Compra'),
    ('venta', 'Venta'),
    ('cambio', 'Cambio de producto'),
    ('produccion', 'Producción'),
    ('disminucion', 'Disminución por producción'),
    ('devolucion', 'Devolución'),
    ('ingreso_interno', 'Ingreso Interno'),
    ('salida_interna', 'Salida Interna'),
)

class Inventory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    document = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.FloatField(default=1)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        product = Product.objects.get(pk=self.product.id)
        if self.movement_type == 'compra' or self.movement_type == 'produccion' or self.movement_type == 'devolucion' or self.movement_type == 'ingreso_interno':
            product.stock += self.quantity
        else: 
            product.stock -= self.quantity
        product.save()
        super(Inventory, self).save(*args, **kwargs)

    def delete(self):
        product = Product.objects.get(pk=self.product.id)
        if self.movement_type == 'compra' or self.movement_type == 'produccion' or self.movement_type == 'devolucion' or self.movement_type == 'ingreso_interno':
            product.stock -= self.quantity
        else: 
            product.stock += self.quantity
        product.save()

        super(Inventory, self).delete()
