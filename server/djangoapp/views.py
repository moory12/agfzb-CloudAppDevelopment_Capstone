import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from .restapis import get_dealers_from_cf, get_dealer_from_cf_by_id, get_dealers_from_cf_by_state, \
    get_dealer_reviews_from_cf, post_request

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
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        load_dotenv()
        dealer_function_url = os.getenv("FUNCTION_DEALER_URL")
        context = {}
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(dealer_function_url)
        # Concat all dealer's short name
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_by_state(request, state):
    if request.method == "GET":
        load_dotenv()
        dealer_function_url = os.getenv("FUNCTION_DEALER_URL")
        url = dealer_function_url
        # Get dealers from the URL
        dealerships = get_dealers_from_cf_by_state(url, state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships_by_id(request, dealer_id):
    if request.method == "GET":
        load_dotenv()
        dealer_function_url = os.getenv("FUNCTION_DEALER_URL")
        url = dealer_function_url
        # Get dealers from the URL
        dealerships = get_dealer_from_cf_by_id(url, dealer_id)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        load_dotenv()
        review_function_url = os.getenv("FUNCTION_REVIEW_URL")
        context = {}
        url = review_function_url
        # Get dealers from the URL
        dealerships = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        context['dealershipDetails'] = dealerships
        context['dealer_id'] = dealer_id
        for dealer in dealerships:
            if dealer.sentiment == 'negative':
                dealer.sentiment = 'negative.png'
            elif dealer.sentiment == 'positive':
                dealer.sentiment = 'positive.png'
            else:
                dealer.sentiment = 'neutral.png'

        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == 'POST':
        print(request.POST)
        car_model = get_object_or_404(CarModel, pk=request.POST['car'])
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["name"] = car_model.name
        review["purchase"] = request.POST['purchasecheck']
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = car_model.carMake.name
        review["car_model"] = car_model.name
        review["car_year"] = car_model.year.year

        json_payload = dict()
        json_payload["REVIEW"] = review
        load_dotenv()
        review_function_url = os.getenv("FUNCTION_REVIEW_URL")
        url = review_function_url
        response = post_request(url=url, json_payload=json_payload)
        return redirect("djangoapp:dealerReview", dealer_id=dealer_id)
    else:
        context = {}
        try:
            load_dotenv()
            url = os.getenv("FUNCTION_DEALER_URL")
            context['dealer'] = get_dealer_from_cf_by_id(url, dealer_id)
            context['cars'] = CarModel.objects.filter(dealer_id=dealer_id)
        except:
            return render(request, 'djangoapp/index.html')

        return render(request, 'djangoapp/add_review.html', context)
