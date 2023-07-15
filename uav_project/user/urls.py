from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from uav_project.rental.views import RentalViewSet
from uav_project.user.views import UserViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")

users_router = NestedDefaultRouter(router, "users", lookup="user")
users_router.register("rentals", RentalViewSet, basename="user-rentals")

main_routers = (router,)
nested_routers = (users_router,)
