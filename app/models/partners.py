from django.db import models

DOCUMENT_TYPE_CHOICES = (
    ('ruc', 'RUC'),
    ('dni', 'DNI'),
    ('ce', 'Cedula Extranjera'),
)
PARTNER_TYPE_CHOICES = (
    ('customer', 'Cliente'),
    ('provider', 'Proveedor'),
    ('cp', 'Cliente y Proveedor'),
)

class Partner(models.Model):
    name = models.CharField(max_length=250)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE_CHOICES, default='customer')
    document_type = models.CharField(max_length=20,choices=DOCUMENT_TYPE_CHOICES, default='ruc')
    document_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
