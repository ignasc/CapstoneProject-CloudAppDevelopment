from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
#from .models import CarDealer
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# CONSTANTS
URL_DEALER_LIST = "https://ignuic-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
URL_DEALER_DETAILS = "https://ignuic-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
URL_POST_REVIEW = "https://ignuic-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"

# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to main page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to index view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this as a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # Login the user and redirect to main page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/index.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(URL_DEALER_LIST)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context = {
            "dealership_list": dealerships,
        }
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    print("Dealer ID: ", dealer_id)
    
    context = {}
    if request.method == "GET":
        dealership_details = get_dealer_by_id_from_cf(URL_DEALER_LIST, dealerId = dealer_id)
        dealership_reviews = get_dealer_reviews_from_cf(
            URL_DEALER_DETAILS + "?id=" + str(dealer_id),# Adding dealer ID to the end of url
            dealerId = dealer_id)#dealership_details[0].id)
        try:
            context = {
                "dealership_review_list": dealership_reviews,
                "dealership_name": dealership_details[0].full_name,
                "dealer_id": dealer_id
            }
            return render(request, 'djangoapp/dealer_details.html', context)
        except Exception as error:
            print(error)
            return HttpResponse ("There was an error in get_dealer_details method")


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    sessionid = request.COOKIES.get('sessionid')
    context = {
        "dealer_id": dealer_id,
    }
    return render(request, 'djangoapp/add_review.html', context)
    #return HttpResponse("add_review method to be implemented")
    # Line above blocks further code execution until it is properly implemented using a submit form
    if sessionid != None:
        print("User is authenticated")
        review = {
            "id": 1114,
            "name": "DEBUG DEALERSHIP",
            "dealership": dealer_id,
            "review": "Great service! Not really, just posting test review",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021,
            "time": datetime.utcnow().isoformat()
        }
        # Prepare payload with review details
        json_payload = {
            "review": review
        }
        # Call post review method to post the review
        result = post_request(URL_POST_REVIEW, json_payload, id = dealer_id)
    else:
        print("User is not authenticated")  
    return HttpResponse("add_review method called. SessionID: " + str(sessionid) + "\n Result of post request: " + str(result.status_code))


def debug(request):# DELETE ME
    return HttpResponse("Debug")
