from rest_framework.permissions import BasePermission, IsAuthenticated


class IsStaffOrSuperuser(BasePermission):
    """Allows access only to staff and superusers."""

    def has_permission(self, request, view) -> bool:
        return request.user and (
            request.user.is_staff or request.user.is_superuser
        )


class UAVPermissionMixin:
    """UAV ViewSet's specific permissions.

    This mixin is used to dynamically set the permissions of the UAV ViewSet
    based on the action.

    When the action is list or retrieve, the permission is IsAuthenticated.
    Otherwise, the permission is IsAuthenticated and IsStaffOrSuperuser.
    """

    def get_permissions(self) -> list:
        if self.action in ("list", "retrieve"):
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated, IsStaffOrSuperuser)
        return [permission() for permission in permission_classes]
