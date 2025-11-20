from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import DriverCreationForm, DriverChangeForm
from .models import User, DriverProfile, Customer


# ------------------------
# 1. Proper User Admin
# ------------------------
class CustomUserAdmin(UserAdmin):
    add_form = DriverCreationForm
    form = DriverChangeForm
    model = User

    list_display = ("email", "username", "is_driver", "is_customer", "is_staff")
    list_filter = ("is_driver", "is_customer", "is_staff", "is_superuser", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("is_driver", "is_customer")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role", {"fields": ("is_driver", "is_customer")}),
    )


admin.site.register(User, CustomUserAdmin)


# ------------------------
# 2. Simple DriverProfile Admin
# ------------------------
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email", "employee_id", "location")

    # Display the related User's username
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

    # Display the related User's email
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"


# ------------------------
# 3. Customer Admin
# ------------------------
admin.site.register(Customer)