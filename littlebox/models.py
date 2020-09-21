from django.db import models

STATUS_CHOICES = (
    ('abierta', 'Abierta'),
    ('cerrada', 'Cerrada'),
)

MOVEMENT_CHOICES = (
    ('entrada', 'Entrada'),
    ('salida', 'Salida')
)

class LittleBox(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='abierta')
    opening_balance = models.FloatField(blank=True)
    closing_balance = models.FloatField(blank=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()

    def cerrar(self):
        suma_de_entradas = 0
        suma_de_salidas = 0
        for item in LittleBoxMovement.objects.filter(little_box=self.id):
            if item.movement_type == 'entrada':
                suma_de_entradas += item.quantity
            else:
                suma_de_salidas += item.quantity

        self.closing_balance = suma_de_entradas - suma_de_salidas
        self.status = 'cerrada'
        self.save(update_fields=['status', 'closing_balance'])

class LittleBoxMovement(models.Model):
    little_box = models.ForeignKey(LittleBox, on_delete=models.PROTECT, limit_choices_to={'status': 'abierta'})
    movement_type = models.CharField(max_length=8, choices=MOVEMENT_CHOICES)
    quantity = models.FloatField()
    movement_details = models.CharField(max_length=200)
    person = models.CharField(max_length=100)