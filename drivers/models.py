from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Custom manager yozamiz
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, phone_number=None, **extra_fields):
        if not phone_number:
            raise ValueError("Foydalanuvchida telefon raqam bo‘lishi shart")
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuserda is_staff=True bo‘lishi kerak")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuserda is_superuser=True bo‘lishi kerak")

        return self.create_user(username, email, password, phone_number, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    objects = CustomUserManager()  # 👈 custom manager uladik

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

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
