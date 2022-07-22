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


# <HINT> Create a plain Python class `DealerReview` to hold review data
