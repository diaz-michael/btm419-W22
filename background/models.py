from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.first_name + " " + self.last_name

class Dealership(models.Model):
    dealer1 = models.CharField(max_length=200, editable=False)
    dealer2 = models.CharField(max_length=200, editable=False)
    dealership = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    def __str__(self):
        return self.dealership.title()

class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=200)
    def __str__(self):
        return self.first_name + " " + self.last_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to = 'images/product')
    def __str__(self):
        return self.name + ",  @$" + str(self.price)