from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Driver as CustomUser
from .models import Customer
import random

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
    


class CustomerChangeForm(UserChangeForm):
    phone_number = forms.CharField(required=False)
    shipping_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User  # This edits the User instance
        fields = ("username", "email", "first_name", "last_name")  # User fields

    def __init__(self, *args, **kwargs):
        # Expect a `user` keyword argument to pre-fill Customer fields
        self.user_instance = kwargs.pop("instance", None)
        super().__init__(*args, instance=self.user_instance, **kwargs)

        if self.user_instance:
            try:
                customer_profile = self.user_instance.customer
                self.fields["phone_number"].initial = customer_profile.phone_number
                self.fields["shipping_address"].initial = customer_profile.shipping_address
            except Customer.DoesNotExist:
                pass
            
    def save(self, commit=True):
        # Save the User fields
        user = super().save(commit=commit)

        # Save or create the Customer profile
        customer_data = {
            "phone_number": self.cleaned_data.get("phone_number"),
            "shipping_address": self.cleaned_data.get("shipping_address"),
        }
        Customer.objects.update_or_create(user=user, defaults=customer_data)

        return user
