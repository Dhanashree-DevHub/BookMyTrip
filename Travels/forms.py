from django import forms
from .models import Booking
from datetime import datetime
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['bus', 'seats_booked', 'journey_date']
        widgets = {
            'bus': forms.HiddenInput(),
            'journey_date': forms.HiddenInput(),
        }

    def clean_seats_booked(self):
        seats = self.cleaned_data['seats_booked']
        bus = self.cleaned_data['bus']
        if seats > bus.available_seats:
            raise forms.ValidationError("Sorry, No seats available!")
        return seats
