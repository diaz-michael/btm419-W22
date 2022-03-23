from pyexpat import model
from django.db import models

# Create your models here.
class inventory_reporting (models.Model):
    time_period = models.IntegerField()
    productID = models.ForeignKey('background.product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    def __str__(self):
        return "#"+ str(self.productID) + "| " + str(self.quantity)