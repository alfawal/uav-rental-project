from rest_framework import viewsets, mixins, filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend


class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("username", "email", "mobile")
    ordering_fields = ("id", "username", "email", "mobile")

    def get_queryset(self):
        if self.request.user.is_superuser:
            ...
