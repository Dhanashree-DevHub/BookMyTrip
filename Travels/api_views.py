from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated

class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class= BookingSerializer
    permission_classes= [IsAuthenticated]