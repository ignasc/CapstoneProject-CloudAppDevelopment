from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    car_make = models.CharField(max_length = 30)
    car_make_description = models.CharField(max_length = 100)
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
    dealer_id = models.IntegerField()
    dealer_name = models.CharField(max_length = 10)
    car_type = models.CharField(max_length = 3, choices = CAR_TYPE_CHOICES)
    car_year = models.IntegerField()
    # Create a toString method for object string representation
    def __str__(self):
        return self.car_type + " (" + car_type + ", " + car_year + ")"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
