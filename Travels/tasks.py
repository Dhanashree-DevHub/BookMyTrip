from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(to_email, bus_name, journey_date, seats, total_price):
    subject= "Bus Booking Confirmation"
    message =  (
        f'Your booking has been confirmed!\n\n'
        f'Bus: {bus_name}\n'
        f'Journey Date: {journey_date}\n'
        f'Seats: {seats}\n'
        f'Total Price: ₹{total_price}\n\n'
        f'Thank you for booking with us!'
    )
    send_mail(subject, message, 'dhanuranade16@gmail.com',[to_email], fail_silently=False)
    
@shared_task
def test_task():
    print("celery is working")
    return "test task complete"