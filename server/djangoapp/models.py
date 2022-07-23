from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Name: ${self.name} \n description: ${self.description}"


class CarModel(models.Model):
    name = models.CharField(max_length=255)
    dealer_id = models.IntegerField()
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    year = models.DateField()
    carMake = models.ForeignKey("CarMake", on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: ${self.name} \n Dealer Id: ${self.dealer_id} \n Type: ${self.type} \n Year${self.year} \n Car " \
               f"Make ${self.carMake.name} "


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data


class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        # Dealer dealership
        self.dealership = dealership
        # Dealer name
        self.name = name
        # Dealer purchase
        self.purchase = purchase
        # Dealer review
        self.review = review
        # purchase_date
        self.purchase_date = purchase_date
        # car_make
        self.car_make = car_make
        # car_model
        self.car_model = car_model
        # car_year
        self.car_year = car_year
        # sentiment
        self.sentiment = ""
        # id
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.name + "\n review:" + self.review


