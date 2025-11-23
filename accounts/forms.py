from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Customer, DriverProfile

User = get_user_model()   # always use this


# ====================================================
# DRIVER CREATION FORM (Creates User + DriverProfile)
# ====================================================
class DriverCreationForm(UserCreationForm):
    location = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.is_driver = True
        if commit:
            user.save()

        # Create the driver profile
        DriverProfile.objects.create(
            user=user,
            location=self.cleaned_data.get("location"),
        )

        return user



# ====================================================
# DRIVER CHANGE FORM (admin editing)
# ====================================================
class DriverChangeForm(UserChangeForm):
    location = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        user = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if user:
            try:
                DriverProfile = user.driverprofile
                self.fields["location"].initial = DriverProfile.location
            except DriverProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        # Save user fields
        user = super().save(commit=commit)

        # Save customer profile fields
        DriverProfile.objects.update_or_create(
            user=user,
            defaults={
                "location": self.cleaned_data.get("location"),
            }
        )

        return user


# ====================================================
# CUSTOMER SIGNUP FORM (Creates User + Customer)
# ====================================================
class CustomerSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=False)
    shipping_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.is_customer = True
        if commit:
            user.save()

        Customer.objects.create(
            user=user,
            phone_number=self.cleaned_data.get("phone_number"),
            shipping_address=self.cleaned_data.get("shipping_address"),
        )

        return user



# ====================================================
# CUSTOMER CHANGE FORM (editing user + profile)
# ====================================================
class CustomerChangeForm(UserChangeForm):
    phone_number = forms.CharField(required=False)
    shipping_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        user = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if user:
            try:
                customer = user.customer
                self.fields["phone_number"].initial = customer.phone_number
                self.fields["shipping_address"].initial = customer.shipping_address
            except Customer.DoesNotExist:
                pass

    def save(self, commit=True):
        # Save user fields
        user = super().save(commit=commit)

        # Save customer profile fields
        Customer.objects.update_or_create(
            user=user,
            defaults={
                "phone_number": self.cleaned_data.get("phone_number"),
                "shipping_address": self.cleaned_data.get("shipping_address"),
            }
        )

        return user

    