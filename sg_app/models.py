from django.db import models

class SacredGrove(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    area_coverage = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name
