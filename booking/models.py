from django.db import models
from drivers.models import SelectedDriver

class Passenger(models.Model):
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    email_or_phone = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    travel_class = models.CharField(max_length=20)
    train_type = models.CharField(max_length=20)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    selected_seat = models.CharField(max_length=10, null=False, blank=True)
    insurance = models.CharField(max_length=50, blank=True, null=True)
    utilities = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=10, null=False, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    book_taxi = models.BooleanField(default=False)
    child_traveler = models.BooleanField(default=False)
    child_name = models.CharField(max_length=100, null=True, blank=True)
    child_dob = models.DateField(null=True, blank=True)
    drop_phone = models.CharField(max_length=20, null=True, blank=True)
    pick_phone = models.CharField(max_length=20, null=True, blank=True)
    special_needs = models.TextField(null=True, blank=True)
    driver = models.ForeignKey(SelectedDriver, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    def __str__(self):
        return f"Booking {self.pk}"
    
class TaxiBooking(models.Model):
    taxi_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='taxi_booking')
    driver = models.ForeignKey(SelectedDriver, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    taxi_date = models.DateField()
    taxi_time = models.TimeField()
    def __str__(self):
        return f"Taxi Booking for {self.booking.passenger.full_name}"
