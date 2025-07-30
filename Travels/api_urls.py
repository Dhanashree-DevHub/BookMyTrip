from rest_framework.routers import DefaultRouter
from .api_views import BookingViewset, BusViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'bookings',BookingViewset)
router.register(r'Bus', BusViewset)

urlpatterns = router.urls