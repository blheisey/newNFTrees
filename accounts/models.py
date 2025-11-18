from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

from django_project import settings

class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <- use this instead of auth.User
        on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Driver(AbstractUser):
    employee_id = models.CharField(max_length=50, unique=True, blank=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    
