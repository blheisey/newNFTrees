from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .models import Customer, DriverProfile

User = get_user_model()


# ==========================================
# DRIVER CREATION FORM (Admin use)
# ==========================================
class DriverCreationForm(forms.ModelForm):
    location = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)

        # Mark as driver
        user.is_driver = True

        # Set unusable first so it's never exposed without us controlling it
        user.set_unusable_password()

        if commit:
            # 1) Save user (so it has a PK)
            user.save()

            # 2) Create DriverProfile (employee_id auto-generated in model)
            profile = DriverProfile.objects.create(
                user=user,
                location=self.cleaned_data.get("location"),
            )

            # 3) Use employee_id as temporary password
            temp_password = str(profile.employee_id)
            user.set_password(temp_password)
            user.save()

            # 4) Email the driver their credentials
            if user.email:
                send_mail(
                    subject="Your Driver Account Login Information",
                    message=(
                        "Hello!\n\n"
                        "Your driver account has been created.\n\n"
                        f"Username: {user.username}\n"
                        f"Temporary password: {temp_password}\n\n"
                        "Please log in and change this password as soon as possible."
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[user.email],
                    fail_silently=True,
                )

            # 5) Attach temp_password so admin can show it in a success message
            user.temp_password = temp_password

        return user


# ==========================================
# DRIVER CHANGE FORM (Admin editing)
# ==========================================
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
                profile = user.driverprofile
                self.fields["location"].initial = profile.location
            except DriverProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        # Save user fields
        user = super().save(commit=commit)

        # Save driver profile fields
        DriverProfile.objects.update_or_create(
            user=user,
            defaults={
                "location": self.cleaned_data.get("location"),
            },
        )

        return user


# ==========================================
# CUSTOMER SIGNUP FORM (Creates User + Customer)
# ==========================================
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


# ==========================================
# CUSTOMER CHANGE FORM (Admin editing)
# ==========================================
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
            },
        )

        return user
