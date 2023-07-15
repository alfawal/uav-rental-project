from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

from uav_project.rental.models import Rental


class UAVModelManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .alias(
                is_rented=models.Exists(
                    Rental.objects.filter(
                        uav_id=models.OuterRef("pk"),
                        start_date__lte=timezone.now(),
                        end_date__gte=timezone.now(),
                    )
                )
            )
        )

    def rented(self) -> models.QuerySet:
        """Returns the UAVs that are currently rented."""
        return self.filter(is_rented=True)

    def not_rented(self) -> models.QuerySet:
        """Returns the UAVs that are currently not rented (Available)."""
        return self.exclude(is_rented=False)
