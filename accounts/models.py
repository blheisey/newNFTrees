from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# ----------------------------------------------------
# Custom User Model
# ----------------------------------------------------
class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ----------------------------------------------------
# Customer Profile
# ----------------------------------------------------
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# ----------------------------------------------------
# Driver Profile
# ----------------------------------------------------
class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
