from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from uav_project.rental.views import RentalViewSet
from uav_project.uav.views import UAVViewSet

router = routers.SimpleRouter()
router.register("uavs", UAVViewSet, basename="uavs")

uav_router = NestedSimpleRouter(router, "uavs", lookup="uav")
uav_router.register("rentals", RentalViewSet, basename="uav-rentals")

urlpatterns = router.urls + uav_router.urls
