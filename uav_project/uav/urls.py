from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from uav_project.rental.views import RentalViewSet
from uav_project.uav.views import UAVViewSet

router = routers.DefaultRouter()
router.register("uavs", UAVViewSet, basename="uavs")

uav_router = NestedDefaultRouter(router, "uavs", lookup="uav")
uav_router.register("rentals", RentalViewSet, basename="uav-rentals")

main_routers = (router,)
nested_routers = (uav_router,)
