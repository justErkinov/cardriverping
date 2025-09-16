from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    

class Vehicle(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle_picture = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    vehicle_brand = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)

    def __str__(self):
        return self.vehicle_number
    
    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'