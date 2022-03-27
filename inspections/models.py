from bdb import effective
from django.db import models
from django.urls import reverse

# Create your models here.
class warranty(models.Model):
    dealershipID = models.ForeignKey('background.Dealership', on_delete=models.PROTECT)
    customerID = models.ForeignKey('background.Customer', on_delete=models.PROTECT)
    products = models.TextField(max_length=200)
    productBundle = models.BooleanField()
    extendedW = models.BooleanField()
    effectiveDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.customerID)

class claim(models.Model):
    warrantyID = models.ForeignKey(warranty, on_delete=models.PROTECT)
    description = models.TextField(max_length=3000)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    STATUS_CHOICES = [
        ('Pn', 'Pending'),
        ('Ap', 'Approved'),
        ('Sb', 'Submitted'),
        ('Pd', 'Paid')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='Pn',
    )
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.warrantyID)

class inspection(models.Model):
    claimID = models.ForeignKey(claim, on_delete=models.PROTECT)
    vin = models.CharField(max_length=200)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.DecimalField(max_digits=4, decimal_places=0)
    colour = models.CharField(max_length=200)
    STATUS_CHOICES = [
        ('Sc', 'Scheduled'),
        ('Cm', 'Completed'),
        ('Ex', 'Expired')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='Sc',
    )
    scheduledDate = models.DateTimeField()
    def list(self):
        return self.id

    def __str__(self):
        return  "#"+ str(self.id) + "| " + str(self.year) + " " + self.colour + " " +  self.make + " " +  self.model

    def get_absolute_url(self):
        return reverse("inspections:detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("inspections:update", kwargs={"id": self.id})