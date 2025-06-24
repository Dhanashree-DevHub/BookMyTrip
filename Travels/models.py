from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Bus(models.Model):
    name = models.CharField(max_length=100)
    source= models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=40)
    available_seats = models.IntegerField(default=40)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}({self.source} to {self.destination})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus= models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats_booked=models.PositiveIntegerField(   validators=[
        MinValueValidator(1),
        MaxValueValidator(40)
    ])
    total_price= models.DecimalField(max_digits=10, decimal_places=2)
    journey_date=models.DateTimeField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def __str__(self):
        return f"{self.user.username} booked {self.seats_booked} seat(s) on {self.bus.name} ({self.journey_date})"

# Create your models here.
