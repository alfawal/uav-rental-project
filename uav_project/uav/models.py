from django.db import models
from django.utils.translation import gettext_lazy as _

from uav_project.uav.managers import UAVModelManager
from uav_project.utils.models import TimestampedModel


class UAVModel(TimestampedModel):
    """Model definition for UAV (Unmanned Aerial Vehicle)."""

    brand = models.CharField(
        max_length=128,
        help_text=_("The name of the UAV (e.g. Bayraktar)."),
    )
    model = models.CharField(
        max_length=128,
        help_text=_(
            "The model of the UAV (e.g. TB2, Akinci, Kizilelma (MIUS), DIHA)."
        ),
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("The weight of the UAV in kilograms."),
    )
    category = models.CharField(
        max_length=128,
        help_text=_("The category of the UAV (e.g. Tactical, MALE, HALE)."),
    )
    description = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=_("A very detailed description of the UAV."),
    )
    daily_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    photo = models.ImageField(
        upload_to="uav_photos",
        blank=True,
        null=True,
    )
    data = models.JSONField(
        blank=True,
        null=True,
        default=None,
        help_text=_(
            "Additional properties of the UAV (e.g. speed, endurance, etc.)."
        ),
    )

    objects = UAVModelManager()

    class Meta:
        """Meta definition for UAV."""

        verbose_name = "Unmanned Aerial Vehicle"
        verbose_name_plural = "Unmanned Aerial Vehicles"

    def __str__(self):
        """Unicode representation of UAV."""
        return (
            f"{self.brand} {self.model} - {self.weight}kg"
            f" | {self.daily_price}"
        )
