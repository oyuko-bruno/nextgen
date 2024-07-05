# views.py
from django.shortcuts import render, redirect
from .models import TaxiDriverApplication

def apply(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        form_data = request.POST
        form_files = request.FILES

        # Create a new TaxiDriverApplication object
        application = TaxiDriverApplication(
            full_name=form_data.get('fullName'),
            phone=form_data.get('phone'),
            email=form_data.get('email'),
            id_number=form_data.get('idNumber'),
            license_number=form_data.get('licenseNumber'),
            issuing_authority=form_data.get('issuingAuthority'),
            valid_until=form_data.get('validUntil'),
            license_class=form_data.get('licenseClass'),
            vehicle_make_model=form_data.get('vehicleMakeModel'),
            year_of_manufacture=form_data.get('yearOfManufacture'),
            registration_number=form_data.get('registrationNumber'),
            background_check=form_data.get('backgroundCheck') == 'on',
            signature=form_data.get('signature'),
            vehicle_photo=form_files.get('vehiclePhoto'),
            insurance_proof=form_files.get('insuranceProof')
        )
        application.save()

        # Pass form data to the success view
        return redirect('application_success', full_name=form_data.get('fullName'))

    return render(request, 'taxi_apply.html')

def application_success(request, full_name):
    # Render the success template with the form data
    return render(request, 'application_success.html', {
        'full_name': full_name,
    })
