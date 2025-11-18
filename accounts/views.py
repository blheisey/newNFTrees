from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomerSignUpForm
from django.shortcuts import render, redirect

class EmployeeSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/employee_signup.html"


def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # or wherever you like
    else:
        form = CustomerSignUpForm()

    return render(request, "registration/signup.html", {"form": form})