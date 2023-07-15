from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from uav_project.rental.views import RentalViewSet
from uav_project.user.views import UserViewSet

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")

users_router = NestedSimpleRouter(router, "users", lookup="user")
users_router.register("rentals", RentalViewSet, basename="user-rentals")

urlpatterns = router.urls + users_router.urls
