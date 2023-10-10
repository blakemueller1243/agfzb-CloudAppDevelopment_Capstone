from django.db import models

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=101)
    description = models.TextField()
    
    # Add any other fields you want for CarMake
    
    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()  # You can change this field type if needed
    TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
        # Add more choices as needed
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    
    # Add any other fields you want for CarModel
    
    def __str__(self):
        return f"{self.car_make.name} - {self.name}"
