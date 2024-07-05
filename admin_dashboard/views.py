from django.shortcuts import render, get_object_or_404, redirect
from drivers.models import SelectedDriver
from authentication.models import CustomUser
from taxi.models import TaxiDriverApplication
from .models import ApprovedDriver

def admin_dashboard(request):
    # Retrieve user data (for demonstration purposes, you might want to add filtering or ordering)
    users = CustomUser.objects.all()
    drivers = TaxiDriverApplication.objects.all()
    approved_drivers = ApprovedDriver.objects.all()  # Retrieve approved drivers

    # Pass user data and approved drivers to the template
    context = {
        'users': users,
        'drivers': drivers,
        'approved_drivers': approved_drivers,  # Include approved drivers in the context
    }
    return render(request, 'admin_dashboard.html', context)

def approve_driver(request, driver_id):
    if request.method == 'POST':
        driver = get_object_or_404(TaxiDriverApplication, pk=driver_id)
        ApprovedDriver.objects.create(
            full_name=driver.full_name,
            phone=driver.phone,
            email=driver.email,
            vehicle_make_model = driver.vehicle_make_model,
            registration_number = driver.registration_number,
            vehicle_photo = driver.vehicle_photo,
            # Add other fields as needed
        )
        driver.delete()
        return redirect('admin_dashboard')  
    return redirect('admin_dashboard')  

def driver_profile(request):
    approved_drivers = ApprovedDriver.objects.all()
    return render(request, 'drivers_profile.html', {'approved_drivers': approved_drivers})
