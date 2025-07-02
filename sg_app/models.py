from django.db import models
from django.contrib.auth.models import User

# Original SacredGrove model (unchanged)
class SacredGrove(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    area_coverage = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)  

    def __str__(self):
        return self.name

# New model to store user-submitted, pending sacred grove details
class PendingSacredGrove(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pending_sacred_groves")
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    area_coverage = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp of submission

    def __str__(self):
        return f"Pending Sacred Grove from {self.user.username}"

    # Method to move the pending grove to the approved table
    def move_to_verified(self):
        sacred_grove = SacredGrove.objects.create(
            name=self.name,
            state=self.state,
            district=self.district,
            latitude=self.latitude,
            longitude=self.longitude,
            area_coverage=self.area_coverage,
            altitude=self.altitude,
            description=self.description,
        )
        return sacred_grove
