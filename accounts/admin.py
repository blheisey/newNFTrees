from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Driver as CustomUser
from .models import Customer

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "employee_id",
        "location",
    ]

    # 👇 these must be inside the class!
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("employee_id", "location")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("employee_id", "location")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer)