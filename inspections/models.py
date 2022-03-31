from bdb import effective
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_vin(value):
    POSITIONAL_WEIGHTS = [8,7,6,5,4,3,2,10,0,9,8,7,6,5,4,3,2]
    ILLEGAL_ALL = ['I', 'O', 'Q']
    ILLEGAL_TENTH = ['U','Z','0']
    LETTER_KEY = dict(
        A=1,B=2,C=3,D=4,E=5,F=6,G=7,H=8,
        J=1,K=2,L=3,M=4,N=5,    P=7,    R=9,
            S=2,T=3,U=4,V=5,W=6,X=7,Y=8,Z=9,
    )

    if len(value) == 17:
        vin = value.upper()

        for char in ILLEGAL_ALL:
            if char in vin:
                raise ValidationError('Field cannot contain "I", "O", or "Q".')

        if vin[9] in ILLEGAL_TENTH:
            raise ValidationError('Field cannot contain "U", "Z", or "0" in position 10.')

        check_digit = vin[8]

        pos=sum=0
        for char in vin:
            value = int(LETTER_KEY[char]) if char in LETTER_KEY else int(char)
            weight = POSITIONAL_WEIGHTS[pos]
            sum += (value * weight)
            pos += 1

        calc_check_digit = int(sum) % 11

        if calc_check_digit == 10:
            calc_check_digit = 'X'

        if str(check_digit) != str(calc_check_digit):
            raise ValidationError('Invalid VIN.')
    else:
        raise ValidationError('Field must be 17 characters.')

# Create your models here.
class warrantyManager(models.Manager):
    def get_queryset(self):
        return super(warrantyManager, self).get_queryset().select_related()

class warranty(models.Model):
    dealershipID = models.ForeignKey('background.Dealership', on_delete=models.PROTECT)
    customerID = models.ForeignKey('background.Customer', on_delete=models.PROTECT)
    products = models.TextField(max_length=200)
    productBundle = models.BooleanField()
    extendedW = models.BooleanField()
    effectiveDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now=True)
    objects = warrantyManager()
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.customerID)

class claimManager(models.Manager):
    def get_queryset(self):
        return super(claimManager, self).get_queryset().select_related()

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
    objects = claimManager()
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.warrantyID)

class inspectionManager(models.Manager):
    def get_queryset(self):
        return super(inspectionManager, self).get_queryset().select_related()

class inspection(models.Model):
    claimID = models.ForeignKey(claim, on_delete=models.PROTECT)
    vin = models.CharField(
        max_length=200,
        validators =[validate_vin])
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
    objects = inspectionManager()
    def list(self):
        return self.id

    def __str__(self):
        return  "#"+ str(self.id) + "| " + str(self.year) + " " + self.colour + " " +  self.make + " " +  self.model

    def get_absolute_url(self):
        return reverse("inspections:detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("inspections:update", kwargs={"id": self.id})