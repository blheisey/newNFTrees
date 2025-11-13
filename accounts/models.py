from django.contrib.auth.models import AbstractUser
from django.db import models

class Driver(AbstractUser):
    employee_id = models.CharField(max_length=50, unique=True, blank=False)
    location = models.CharField(max_length=100, blank=True, null=True)
