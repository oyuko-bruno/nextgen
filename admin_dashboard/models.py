from django.db import models

class ApprovedDriver(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, default='000-000-0000') 
    email = models.EmailField()
    vehicle_make_model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    vehicle_photo = models.ImageField(upload_to='vehicle_photos/')
    # Add any additional fields if needed

    def __str__(self):
        return self.full_name
