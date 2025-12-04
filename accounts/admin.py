from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages

from .models import User, DriverProfile, Customer
from .forms import DriverCreationForm, DriverChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = DriverCreationForm
    form = DriverChangeForm
    model = User

    list_display = ("email", "username", "is_driver", "is_customer", "is_staff")
    list_filter = ("is_driver", "is_customer", "is_staff", "is_superuser")

    # For editing existing users
    fieldsets = UserAdmin.fieldsets + (
        ("Roles", {"fields": ("is_driver", "is_customer")}),
    )

    # For adding new users in admin
    # ⚠️ Note: No password fields here; password is auto-generated.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email"),
        }),
        ("Roles", {"fields": ("is_driver", "is_customer")}),
    )

    def save_model(self, request, obj, form, change):
        """
        - For new users created via DriverCreationForm:
            * is_driver is already set True in the form
            * DriverProfile and password are already created
            * temp_password is attached to obj
        - Here we just show the popup if present.
        """
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        # Show temporary password if the form attached it
        if hasattr(obj, "temp_password"):
            messages.success(
                request,
                f"Driver account created! Temporary password: {obj.temp_password}"
            )


admin.site.register(User, CustomUserAdmin)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_id", "location")


admin.site.register(DriverProfile, DriverProfileAdmin)
admin.site.register(Customer)

