from rest_framework import viewsets
from .models import Booking, Bus
from .serializers import BookingSerializer, BusSerializer
from rest_framework.permissions import IsAuthenticated

class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class= BookingSerializer
    permission_classes= [IsAuthenticated]
    
    
class BusViewset(viewsets.ModelViewSet):
    queryset= Bus.objects.all()
    serializer_class= BusSerializer
    
class BusViewset(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class= BusSerializer
    permission_classes=[IsAuthenticated]