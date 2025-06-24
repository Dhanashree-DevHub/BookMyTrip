from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['bus', 'seats_booked', 'journey_date']
        widgets = {
            'bus': forms.HiddenInput(),
            'journey_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bus' in self.initial:
            bus = self.initial['bus']
            self.fields['seats_booked'].widget = forms.NumberInput(attrs={
                'min': 1,
                'max': bus.available_seats,
                'class': 'form-control'
            })

    def clean_seats_booked(self):
        seats = self.cleaned_data.get('seats_booked')
        bus = self.cleaned_data.get('bus')

        if seats is None or bus is None:
            raise ValidationError("Invalid booking request.")

        if seats < 1:
            raise ValidationError("You must book at least 1 seat.")

        if seats > bus.available_seats:
            raise ValidationError(f"Only {bus.available_seats} seat(s) available.")

        if seats > 40:
            raise ValidationError("You cannot book more than 40 seats.")

        return seats
# from django import forms
# from .models import Booking
# from datetime import datetime
# from django.core.exceptions import ValidationError

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['bus', 'seats_booked', 'journey_date']
#         widgets = {
#             'bus': forms.HiddenInput(),
#             'journey_date': forms.HiddenInput(),
#         }

#     def clean_seats_booked(self):
#         seats = self.cleaned_data['seats_booked']
#         bus = self.cleaned_data['bus']
#         if seats > bus.available_seats:
#             raise forms.ValidationError("Sorry, No seats available!")
#         return seats
