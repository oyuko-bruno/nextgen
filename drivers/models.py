from django.db import models

class SelectedDriver(models.Model):
    driver_id = models.IntegerField(primary_key=True)  # Specify driver_id as the primary key
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    vehicle_make_model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20)
    vehicle_photo = models.ImageField(upload_to='driver_photos/')
    selected = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name  # Return a string representation for admin interface or debugging purposes
