from django.db import models

from .documents import Document
from .inventories import Inventory
from .recipes import MaterialList


class ProductionOrder(models.Model):
    STATUS_CHOICES = (
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('producida', 'Producida'),
    )
    document_type = models.ForeignKey(Document, on_delete=models.PROTECT, limit_choices_to={'abbreviation': 'OP'})
    document_number = models.CharField(max_length=15)
    date = models.DateTimeField()
    material_list = models.ForeignKey(MaterialList, on_delete=models.PROTECT)
    quantity_to_produce = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrador')

    def stock_available(self, factor):
        res = True
        for item in self.material_list.components.all():
            if not item.product.stock >= factor*item.quantity:
                res = False
                break
        return res

    def produce(self, factor):
        """ Consumir los insumos de la lista de materiales. """
        for item in self.material_list.components.all():
            Inventory.objects.create(
                movement_type='disminucion',
                product=item.product,
                quantity=factor*item.quantity,
                document=self.document_type.abbreviation+self.document_number
            )
        """ Cargar lo producido al inventario. """
        Inventory.objects.create(
            movement_type='produccion',
            product=item.material_list.product,
            quantity=self.quantity_to_produce,
            document=self.document_type.abbreviation+self.document_number
        )

    def save(self, *args, **kwargs):
        if not self.id:
            doc = Document.objects.get(id=self.document_type.id)
            self.document_number = doc.serial + '-' + str(doc.current_number)
            doc.current_number += 1
            doc.save()

        if self.status == 'confirmada':
            """ Calcular el factor a usar en cada consumo de insumos
                Esto se consigue dividiendo la cantidad de productos a producir con
                la cantidad de productos de la lista de materiales (receta) """
            factor = self.quantity_to_produce/self.material_list.quantity_of_products
            there_is_stock = self.stock_available(factor)
            if there_is_stock:
                self.produce(factor)
                self.status = 'producida'
            else:
                self.status = 'borrador'
        
        super(ProductionOrder, self).save(*args, **kwargs)
