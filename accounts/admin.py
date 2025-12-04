from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import DriverChangeForm, DriverCreationForm
from .models import Customer, DriverProfile, User


class CustomUserAdmin(UserAdmin):
    add_form = DriverCreationForm
    form = DriverChangeForm
    model = User

    list_display = ("email", "username", "is_driver", "is_customer", "is_staff")
    list_filter = ("is_driver", "is_customer", "is_staff", "is_superuser")

    fieldsets = UserAdmin.fieldsets + (
        ("Roles", {"fields": ("is_driver", "is_customer")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Roles", {"fields": ("is_driver", "is_customer")}),
    )


admin.site.register(User, CustomUserAdmin)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_id", "location")

admin.site.register(DriverProfile, DriverProfileAdmin)
admin.site.register(Customer)
