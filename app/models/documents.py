from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=3)
    serial = models.CharField(max_length=3)
    current_number = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
