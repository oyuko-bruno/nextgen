from django.contrib import admin
from .models import Passenger, Booking, TaxiBooking, SelectedDriver

admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(TaxiBooking)
admin.site.register(SelectedDriver)
