from rest_framework.routers import DefaultRouter
from .api_views import BookingViewset
from django.urls import path, include

router = DefaultRouter()
router.register(r'bookings',BookingViewset)

urlpatterns = router.urls