from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
        else:
            messages.error(request, 'Invalid username or password')
    return redirect('djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "POST":  # You can use a POST request for logout
        logout(request)  # Call the logout function to log the user out
        messages.success(request, 'Logout successful!')
    return redirect('djangoapp/index.html')

def registration_request(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('signup')  # Redirect back to the signup page

        # Create a new user account
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

        # Optionally, you can log in the user automatically after registration
        # from django.contrib.auth import login
        # login(request, user)

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('djangoapp/index.html')  # Redirect to the login page

    return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

