from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    car_make = models.CharField(max_length = 30, default = 'Not Specified')
    car_make_description = models.CharField(max_length = 100, default = 'Not Specified')
    # Create a toString method for object string representation
    def __str__(self):
        return self.car_make


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    # Choices defined as constants
    SEDAN = "SDN"
    SUV = "SUV"
    WAGON = "WGN"
    CAR_TYPE_CHOICES = [
        (SEDAN, "SEEDAN"),
        (SUV, "SUV"),
        (WAGON, "WAGON"),
    ]
    car_model = models.ForeignKey(CarMake, on_delete = models.CASCADE) # Many-to-one relationship - One make can have many models
    dealer_name = models.CharField(max_length = 20, default = 'Not Specified')
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length = 3, choices = CAR_TYPE_CHOICES)
    car_year = models.IntegerField()
    # Create a toString method for object string representation
    def __str__(self):
        return self.car_model.car_make + " (" + self.car_type + ", " + str(self.car_year) + ")"

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
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
    def __str__(self):
        return "This is the review entry of a dealer " + self.dealership
