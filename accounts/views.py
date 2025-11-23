from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import DriverCreationForm, CustomerSignUpForm
from django.shortcuts import render, redirect
from .forms import CustomerChangeForm, DriverChangeForm

class EmployeeSignUpView(CreateView):
    form_class = DriverCreationForm
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



def edit_customer_profile(request):
    if request.method == "POST":
        form = CustomerChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")  # redirect to profile page
    else:
        form = CustomerChangeForm(instance=request.user)

    return render(request, "registration/customer_change_form.html", {"form": form})



def edit_driver_profile(request):
    if request.method == "POST":
        form = DriverChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")  # redirect to profile page
    else:
        form = DriverChangeForm(instance=request.user)

    return render(request, "registration/driver_change.html", {"form": form})