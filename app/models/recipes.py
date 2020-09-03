from django.db import models
from django.db.models import Q

from .products import Product

class MaterialList(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={'is_manufactured': True})
    quantity_of_products = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
     
class Component(models.Model):
    material_list = models.ForeignKey(MaterialList, on_delete=models.CASCADE, related_name='components')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to=Q(could_be_bought=True) | Q(is_manufactured=True))
    quantity = models.FloatField(default=0)
