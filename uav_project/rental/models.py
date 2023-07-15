from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from uav_project.utils.models import TimestampedModel


class Rental(TimestampedModel):
    """Model definition for Rental."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rentals",
    )
    uav = models.ForeignKey(
        "uav.UAVModel",
        on_delete=models.PROTECT,
        related_name="rentals",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        """Meta definition for Rental."""

        verbose_name = "Rental"
        verbose_name_plural = "Rentals"

    def __str__(self) -> str:
        """Unicode representation of Rental."""
        return (
            f"{self.user.username} - {self.uav.model}"
            f" - {self.start_date} - {self.end_date}"
        )

    def get_total_price(self) -> str:
        """Calculate the total price of the rental."""
        return str((self.end_date - self.start_date).days * self.price)

    def clean(self) -> None:
        """Validate the rental start and end date."""
        if self.start_date > self.end_date:
            raise ValidationError(
                "The start date must be earlier the end date."
            )

    def save(self, *args, **kwargs) -> None:
        """Set the price of the rental on creation and don't allow updating it."""
        if not self.pk:
            self.price = self.uav.daily_price
        else:
            old_price = Rental.objects.get(pk=self.pk).price
            if old_price != self.price:
                self.price = old_price
        self.full_clean()
        super().save(*args, **kwargs)
