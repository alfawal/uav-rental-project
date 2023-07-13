from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UAVUser(AbstractUser):
    """Customizes the default Django User model.

    Adds a new field called is_customer to the default Django User model.
    The field is_customer is used to distinguish between customers.
    superusers (is_superuser): users that don't need a permission (Admins).
    staff members (is_staff): users that can access the admin site.

    Why not use Django's Group/Permission model?
    Because it's not flexible enough in our case. Its a single role
    that we wanted to add. Having a model that we must query and manage would
    be an overkill.
    """

    is_customer = models.BooleanField(
        _("customer status"),
        default=False,
        help_text=_("Designates whether the user is a customer."),
    )

    def clean(self) -> None:
        """Validates the role of the user.

        Raises:
            ValidationError: If the user has more than one role or
                no role at all.

        Returns:
            None
        """
        # Count how many roles are set to True.
        # NOTE: True is 1 and False is 0 in Python.
        true_roles_count = sum(
            (
                self.is_staff,
                self.is_customer,
                self.is_superuser,
            )
        )

        if true_roles_count > 1:
            raise ValidationError("The user can only have one role at a time.")

        if true_roles_count == 0:
            raise ValidationError("The user must have at least one role.")

    def save(self, *args, **kwargs) -> None:
        """Validates the user before saving."""
        self.full_clean()
        super().save(*args, **kwargs)
