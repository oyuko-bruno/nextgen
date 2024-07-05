from django.db import models

class TaxiDriverApplication(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='000-000-0000') 
    email = models.EmailField()
    id_number = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50)
    issuing_authority = models.CharField(max_length=100)
    valid_until = models.DateField()
    license_class = models.CharField(max_length=50)
    vehicle_make_model = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField()
    registration_number = models.CharField(max_length=50)
    background_check = models.BooleanField()
    signature = models.CharField(max_length=100)
    vehicle_photo = models.ImageField(upload_to='vehicle_photos/')
    insurance_proof = models.ImageField(upload_to='insurance_proofs/')

    # Add any additional fields if needed
