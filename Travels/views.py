from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Booking
from .forms import BookingForm
from django.contrib import messages
from django.db.models import Sum
from .models import Bus, Booking
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .tasks import send_booking_confirmation_email

@login_required
def home(request):
    sources = Bus.objects.values_list('source', flat=True).distinct()
    destinations = Bus.objects.values_list('destination', flat=True).distinct()
    buses = None

    if request.method == "GET" and 'from' in request.GET:
        selected_source = request.GET.get('from')
        selected_destination = request.GET.get('to')
        date =request.GET.get('date')

        if selected_source and selected_destination:
            buses = Bus.objects.filter(
                source=selected_source,
                destination=selected_destination
            )
    
    return render(request, 'Travels/home.html', {
        'sources': sources,
        'destinations': destinations,
        'buses': buses,
    })

def search_buses(request):
    source = request.GET.get('from')
    destination = request.GET.get('to')
    journey_date = request.GET.get('date')
    request.session['journey_date']= journey_date

    buses = Bus.objects.filter(source=source, destination=destination)

    for bus in buses:
        booked = Booking.objects.filter(bus=bus, journey_date=journey_date).aggregate(Sum('seats_booked'))['seats_booked__sum'] or 0
        bus.available_seats = bus.total_seats - booked

    return render(request, 'Travels/search_results.html', {'buses': buses, 'journey_date': journey_date})

@login_required
def book_ticket(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    journey_date = request.GET.get('date') or request.session.get('journey_date')
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.journey_date = journey_date
            booking.total_price= booking.seats_booked * bus.price_per_seat
            bus.save()
            booking.save()
            send_booking_confirmation_email.delay(
                to_email=request.user.email,
                bus_name=bus.name,
                journey_date=str(booking.journey_date),
                seats=booking.seats_booked,
                total_price=booking.total_price
            )
            messages.success(request, "Booking successful")
            return redirect('my_trips')
        else:
            messages.error(request, "No seats available")
    else:
        form= BookingForm(initial={'bus': bus, 'journey_date': journey_date})
    
    return render(request, 'Travels/book_ticket.html', {'form': form, 'bus': bus, 'journey_date':journey_date})

def my_trips(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'Travels/my_trips.html', {'bookings': bookings})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking canceled successfully")
    return redirect('my_trips')

def modify_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_price = booking.seats_booked * booking.bus.price_per_seat
            booking.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('my_trips')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'Travels/modify_booking.html', {
        'form': form,
        'bus': booking.bus,
        'journey_date': booking.journey_date
    })

@csrf_exempt
def proceed_to_pay(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.payment_status="Paid"
        booking.save()
        messages.success(request, "Payment successful!!")
        return redirect('my_trips')

    return render(request, 'Travels/proceed_to_pay.html',{
        'booking': booking
    })


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Confirm_password = request.POST.get('confirm_password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'Travels/signup.html')

        if password != Confirm_password:
            messages.error(request, "Password do not match")
            return render(request, 'Travels/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist")
            return render(request, 'Travels/signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'Travels/signup.html')
        