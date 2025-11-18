from django.urls import path
from .views import customer_signup, EmployeeSignUpView, CustomerChangeForm




urlpatterns = [
    path("signup/", customer_signup, name="signup"),
    path("employee_signup/", EmployeeSignUpView.as_view(), name="employee_signup"),
    path("customer_change/", CustomerChangeForm,  name = "customer_change"),
]
