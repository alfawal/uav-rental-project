from django.db import models


class TimestampedModel(models.Model):
    """Self-managed timestamped model.

    An abstract base class model that provides self-managed "created_at"
    and "updated_at" fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for TimestampedModel."""

        abstract = True
