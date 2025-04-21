from django.urls import path
from . import views
from .views import home, book_ticket, my_trips

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_buses, name='search_buses'),
    path('book/<int:bus_id>/', book_ticket, name='book_ticket'),
    path('my-trips/', my_trips, name='my_trips'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('modify-booking/<int:booking_id>/', views.modify_booking, name='modify_booking'),
    path('proceed-to-pay/<int:booking_id>', views.proceed_to_pay, name='proceed_to_pay'),
    path('signup/', views.signup, name='signup')
]
