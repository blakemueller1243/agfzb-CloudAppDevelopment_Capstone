from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealer_by_id, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib import messages
import requests

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
    return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "POST":  # You can use a POST request for logout
        logout(request)  # Call the logout function to log the user out
        messages.success(request, 'Logout successful!')
    return redirect('djangoapp:index')

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
        return redirect('djangoapp:index')  # Redirect to the login page

    return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://blakemueller-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"

        # Make an HTTP GET request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the JSON response
            dealerships = json.loads(response.text)

            # Create a list of dictionaries with short_name and id
            dealer_data = [{'short_name': dealer['short_name'], 'id': dealer['id']} for dealer in dealerships]

            # Pass the JSON data to the template
            return render(request, 'djangoapp/index.html', {'dealers': dealer_data})
        else:
            print("Failed to retrieve data. Status code:", response.status_code)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Replace with your actual API endpoint for dealer details
        dealer_url = f"https://blakemueller-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"

        # Replace with your actual API endpoint for dealer reviews
        reviews_url = f"https://blakemueller-3001.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/{dealer_id}/reviews"
        

        # Make an API request to get dealer details
        dealer_response = requests.get(dealer_url)
        reviews_response = requests.get(reviews_url)
        print(dealer_response)
        print(reviews_response)

        if dealer_response.status_code == 200 and reviews_response.status_code == 200:
            # Parse the JSON response for dealer details
            dealer_data = json.loads(dealer_response.text)
            print(dealer_data)
            # Parse the JSON response for dealer reviews
            reviews_data = json.loads(reviews_response.text)
            print(reviews_data)
            # Extract dealer information
            dealer_id = dealer_data[0].get("id", "")
            dealer_name = dealer_data[0].get("full_name", "")
            dealer_location = dealer_data[0].get("address", "")
            dealer_city = dealer_data[0].get("city", "")
            dealer_state = dealer_data[0].get("state", "")
            dealer_zip = dealer_data[0].get("zip", "")

            # Extract reviews data
            reviews = []
            for review_data in reviews_data:
                review = {
                    'review': review_data.get("review", ""),
                    'sentiment': review_data.get("sentiment", ""),
                }
                reviews.append(review)

            context = {
                'dealer_id': dealer_id,
                'dealer_name': dealer_name,
                'dealer_location': dealer_location,
                'dealer_city': dealer_city,
                'dealer_state': dealer_state,
                'dealer_zip': dealer_zip,
                'reviews': reviews,
            }
            return render(request, 'djangoapp/dealer_details.html', context)
        else:
            return HttpResponse("Dealer details or reviews not found or an error occurred")



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

