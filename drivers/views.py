from django.shortcuts import render, redirect
from .models import SelectedDriver

def store_selected_driver(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        request.session['selected_driver_id'] = driver_id
        request.session['selected_driver_full_name'] = request.POST.get('full_name')
        request.session['selected_driver_phone'] = request.POST.get('phone')
        request.session['selected_driver_email'] = request.POST.get('email')
        request.session['selected_driver_vehicle_make_model'] = request.POST.get('vehicle_make_model')
        request.session['selected_driver_registration_number'] = request.POST.get('registration_number')
        request.session['selected_driver_vehicle_photo'] = request.POST.get('vehicle_photo')

        # Optionally, you can save to database (uncomment if you need to save to SelectedDriver model)
        selected_driver = SelectedDriver(
            driver_id=driver_id,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            vehicle_make_model=request.POST.get('vehicle_make_model'),
            registration_number=request.POST.get('registration_number'),
            vehicle_photo=request.POST.get('vehicle_photo'),
            selected=True
        )
        selected_driver.save()

        return redirect('booking')  # Redirect to booking page after selecting a driver

    return redirect('select_driver')  # Redirect to select_driver page if not a POST request
