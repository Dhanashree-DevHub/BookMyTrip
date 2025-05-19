from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bus, Booking
from datetime import date

class BookingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.bus = Bus.objects.create(name='Test Bus', source='Pune', destination='Mumbai', total_seats=40, price_per_seat=100)
        self.booking = Booking.objects.create(user=self.user, bus=self.bus, seats_booked=2, total_price=200, journey_date='2025-06-01')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/home.html')

    def test_search_buses_view(self):
        response = self.client.get(reverse('search_buses'), {
            'from': 'Pune',
            'to': 'Mumbai',
            'date': '2025-06-01'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/search_results.html')

    def test_book_ticket_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('book_ticket', args=[self.bus.id]), {'date': '2025-06-01'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/book_ticket.html')

    def test_book_ticket_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('book_ticket', args=[self.bus.id]), {
            'bus': self.bus.id,
            'journey_date': '2025-06-01',
            'seats_booked': 2
        })
        self.assertRedirects(response, reverse('my_trips'))
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 2)  # 1 existing + 1 new

    def test_my_trips_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('my_trips'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/my_trips.html')

    def test_cancel_booking(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_trips'))
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_modify_booking_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('modify_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/modify_booking.html')

    def test_modify_booking_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('modify_booking', args=[self.booking.id]), {
            'bus': self.bus.id,
            'journey_date': '2025-06-01',
            'seats_booked': 3
        })
        self.assertRedirects(response, reverse('my_trips'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.seats_booked, 3)

    def test_proceed_to_pay_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('proceed_to_pay', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_trips'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.payment_status, 'Paid')

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Travels/signup.html')

    def test_signup_view_post_valid(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'user1',
            'email': 'email@example.com',
            'password': 'pass1',
            'confirm_password': 'wrongpass'
        })
        self.assertContains(response, "Password do not match")

    def test_signup_existing_username(self):
        User.objects.create_user(username='existinguser', password='12345')
        response = self.client.post(reverse('signup'), {
            'username': 'existinguser',
            'email': 'e@example.com',
            'password': '12345',
            'confirm_password': '12345'
        })
        self.assertContains(response, "Username already exist")



    

# Create your tests here.
# Dhanashri, dhanu16@gmail.com, dhanu@555