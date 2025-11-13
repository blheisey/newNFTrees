from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Driver as CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "employee_id",
            "location",
        ) # new
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "employee_id",
            "location",
) # new