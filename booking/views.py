from django.shortcuts import render, redirect, get_object_or_404
from .models import Passenger, Booking, TaxiBooking, SelectedDriver

def booking_page(request):
    selected_driver = None

    if 'selected_driver_id' in request.session:
        driver_id = request.session['selected_driver_id']
        selected_driver = SelectedDriver.objects.get(pk=driver_id)

    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('adultName')
        dob = request.POST.get('dob')
        email_or_phone = request.POST.get('booking_email_or_phone')
        book_taxi = 'bookTaxi' in request.POST
        pickup_location = request.POST.get('pickupLocation') if book_taxi else None
        dropoff_location = request.POST.get('dropoffLocation') if book_taxi else None
        taxi_date = request.POST.get('taxiDate') if book_taxi else None
        taxi_time = request.POST.get('taxiTime') if book_taxi else None

        # Calculate prices
        travel_class = request.POST.get('travelClass')
        train_type = request.POST.get('trainType')
        utilities = request.POST.get('utilities')
        insurance_type = request.POST.get('insurance')

        ticket_price = calculate_ticket_price(travel_class, train_type)
        insurance_price = calculate_insurance_price(insurance_type)
        wifi_price = calculate_wifi_price(utilities)
        snack_price = calculate_snack_price(utilities)
        wifi_snack_price = calculate_wifi_snack_price(utilities)
        taxi_price = calculate_taxi_price(book_taxi)  # Calculate taxi price here

        total_price = (
            ticket_price +
            insurance_price +
            wifi_price +
            snack_price +
            wifi_snack_price +
            taxi_price
        )

        # Save Passenger
        passenger = Passenger.objects.create(
            full_name=full_name,
            dob=dob,
            email_or_phone=email_or_phone
        )

        # Save Booking
        booking = Booking.objects.create(
            passenger=passenger,
            travel_class=travel_class,
            train_type=train_type,
            from_station=request.POST.get('from'),
            to_station=request.POST.get('to'),
            departure_date=request.POST.get('date'),
            departure_time=request.POST.get('time'),
            selected_seat=request.POST.get('selectedSeatInput'),
            insurance=insurance_type,
            utilities=utilities,
            total_price=total_price,  # Save the calculated total price
            payment_method=request.POST.get('paymentMethod'),
            book_taxi=book_taxi,
            child_traveler=bool(request.POST.get('childName')),
            child_name=request.POST.get('childName'),
            child_dob=request.POST.get('childAge'),
            drop_phone=request.POST.get('drop'),
            pick_phone=request.POST.get('pick'),
            special_needs=request.POST.get('specialNeeds'),
        )

        # Save Taxi Booking if applicable
        if book_taxi and selected_driver:
            # Create TaxiBooking instance with taxi_price included
            taxi_booking = TaxiBooking.objects.create(
                booking=booking,
                driver=selected_driver,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                taxi_date=taxi_date,
                taxi_time=taxi_time,
                taxi_price=taxi_price  # Save taxi_price here
            )

        # Clear selected driver from session
        request.session.pop('selected_driver_id', None)
        request.session.pop('selected_driver_full_name', None)
        request.session.pop('selected_driver_phone', None)
        request.session.pop('selected_driver_email', None)
        request.session.pop('selected_driver_vehicle_make_model', None)
        request.session.pop('selected_driver_registration_number', None)
        request.session.pop('selected_driver_vehicle_photo', None)

        return redirect('confirm_booking', booking_id=booking.id)

    return render(request, 'booking.html', {'selected_driver': selected_driver})

def calculate_ticket_price(travel_class, train_type):
    # Implement your ticket price calculation logic here
    # Example implementation:
    if travel_class == 'first':
        if train_type == 'Inter-County':
            return 2500
        elif train_type == 'Afternoon':
            return 4500
        elif train_type == 'Night':
            return 4500
    elif travel_class == 'economy':
        if train_type == 'Inter-County':
            return 2000
        elif train_type == 'Afternoon':
            return 4000
        elif train_type == 'Night':
            return 4000
    return 0

def calculate_insurance_price(insurance_type):
    if insurance_type == 'premium':
        return 2000
    elif insurance_type == 'basic':
        return 500
    return 0

def calculate_wifi_price(utilities):
    if utilities == 'wifi':
        return 200
    return 0

def calculate_snack_price(utilities):
    if utilities == 'snack':
        return 800
    return 0

def calculate_wifi_snack_price(utilities):
    # Implement your Wi-Fi and Snacks price calculation logic here
    # Example implementation:
    if utilities == 'wifiSnack':
        return 800
    return 0

def calculate_taxi_price(book_taxi):
    # Implement your taxi price calculation logic here
    # Example implementation:
    if book_taxi:
        return 500  # Replace with your actual taxi price calculation logic
    return 0

def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    taxi_booking = TaxiBooking.objects.filter(booking=booking).first()
    selected_driver = taxi_booking.driver if taxi_booking else None

    # Calculate prices again based on the booking details
    ticket_price = calculate_ticket_price(booking.travel_class, booking.train_type)
    insurance_price = calculate_insurance_price(booking.insurance)
    wifi_price = calculate_wifi_price(booking.utilities)
    snack_price = calculate_snack_price(booking.utilities)
    wifi_snack_price = calculate_wifi_snack_price(booking.utilities)
    taxi_price = taxi_booking.taxi_price if taxi_booking else 0  # Corrected logic here

    context = {
        'booking': booking,
        'taxi_booking': taxi_booking,
        'selected_driver': selected_driver,
        'ticket_price': ticket_price,
        'insurance_price': insurance_price,
        'wifi_price': wifi_price,
        'snack_price': snack_price,
        'wifi_snack_price': wifi_snack_price,
        'taxi_price': taxi_price,
    }

    return render(request, 'confirm_booking.html', context)

def select_driver_view(request):
    drivers = SelectedDriver.objects.all()
    return render(request, 'drivers_profile.html', {'drivers': drivers})
