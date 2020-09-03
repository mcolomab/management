from django.db import models

PRODUCT_TYPE_CHOICES = (
    ('almacenable', 'Almacenable'),
    ('servicio', 'Servicio'),
    ('consumible', 'Consumible'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    could_be_sold = models.BooleanField()
    could_be_bought = models.BooleanField()
    is_manufactured = models.BooleanField()
    product_type = models.CharField(max_length=30,choices=PRODUCT_TYPE_CHOICES, default='almacenable')
    price = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    stock = models.FloatField(default=0)

    class Meta:
        ordering = ['-stock']

    def __str__(self):
        return self.name
    
    def terminado_o_insumo(self):
        if self.could_be_sold and self.is_manufactured:
            return 'Terminado'
        elif self.is_manufactured:
            return 'Preparado'
        elif self.could_be_bought:
            return 'Insumo'
        else:
            return self.product_type