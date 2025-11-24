from django.urls import path, include
from .views import customer_signup, EmployeeSignUpView, edit_customer_profile, edit_driver_profile, employee_portal




urlpatterns = [
    path("signup/", customer_signup, name="signup"),
    path("employee/", employee_portal, name="employee_portal"),
    path("employee_signup/", EmployeeSignUpView.as_view(), name="employee_signup"),
    path("customer_change/", edit_customer_profile,  name = "customer_change"),
    path("driver_change/", edit_driver_profile,  name = "driver_change"),
]
