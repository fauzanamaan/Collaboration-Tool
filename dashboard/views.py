# Importing the render and redirect functions from the django.shortcuts module
from django.shortcuts import render, redirect
# Importing the login_required decorator from the django.contrib.auth.decorators module
from django.contrib.auth.decorators import login_required



def dashboard(request):
    # Renders the dashboard template
    return render(request, 'dashboard/dashboard.html')


def frontpage(request):
    return redirect('dashboard')  # Redirects to the dashboard view
