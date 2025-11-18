from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Driver as CustomUser
from .models import Customer

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
        


User = get_user_model()   # always use this, respects AUTH_USER_MODEL


class CustomerSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=False)
    shipping_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "employee_id")  # fields for the User table

    def save(self, commit=True):
        # Create User first
        user = super().save(commit=commit)

        # Create Customer profile
        Customer.objects.create(
            user=user,
            phone_number=self.cleaned_data.get("phone_number"),
            shipping_address=self.cleaned_data.get("shipping_address"),
        )

        return user
    

