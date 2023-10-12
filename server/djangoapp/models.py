from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()

    TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    ]
    model_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return f"Car Make: {self.car_make.name}, Name: {self.name}, Dealer ID: {self.dealer_id}, Model Type: {self.model_type}, Year: {self.year}"

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

class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealer dealership
        self.dealership = dealership
        # Reviewer's name
        self.name = name
        # Purchase type
        self.purchase = purchase
        # Review text
        self.review = review
        # Purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Sentiment of the review
        self.sentiment = sentiment
        # Dealer ID
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.dealership
