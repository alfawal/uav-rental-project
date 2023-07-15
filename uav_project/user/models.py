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

    class Meta:
        """Meta definition for UAVUser."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self) -> None:
        """Validates the role of the user.

        A user can have multiple admin roles (e.g. is_staff and is_superuser)
        but cannot have both admin and customer roles at the same time.

        Raises:
            ValidationError: If the user has no role or has administrative
                and customer roles at the same time.

        Returns:
            None
        """
        admin_roles = (
            self.is_staff,
            self.is_superuser,
        )
        customer_roles = (self.is_customer,)
        all_roles = admin_roles + customer_roles

        has_no_role = not any(all_roles)
        if has_no_role:
            raise ValidationError("The user must have at least one role.")

        is_admin_and_customer = any(admin_roles) and any(customer_roles)
        if is_admin_and_customer:
            raise ValidationError(
                "The user cannot be an admin and a customer."
            )

    def save(self, *args, **kwargs) -> None:
        """Validates the user before saving."""
        # self.full_clean()
        super().save(*args, **kwargs)
