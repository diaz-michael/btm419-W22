from unicodedata import decimal
from django.db import models

# Create your models here.
class order_form(models.Model):
    dealershipID = models.ForeignKey('background.Dealership', on_delete=models.PROTECT)
    salespersonID = models.ForeignKey('background.employee', on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.dealershipID) + " via: " + str(self.salespersonID)

class order(models.Model):
    order_formID = models.ForeignKey(order_form, on_delete=models.PROTECT)
    productID = models.ForeignKey('background.product', on_delete=models.PROTECT)
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    quantity = models.IntegerField()
    def __str__(self):
        return "#"+ str(self.id) + "| " + str(self.productID)