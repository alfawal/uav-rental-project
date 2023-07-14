from django.db import models
from django.utils import timezone


class UAVModelManager(models.Manager):
    def rented(self) -> models.QuerySet:
        """Returns the UAVs that are currently rented."""
        return self.filter(rentals__end_date__gt=timezone.now()).distinct()

    def not_rented(self) -> models.QuerySet:
        """Returns the UAVs that are currently not rented (Available)."""
        return self.exclude(rentals__end_date__gt=timezone.now()).distinct()
