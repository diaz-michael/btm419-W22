from django.db import models
from django.urls import reverse

# Create your models here.
class order_form(models.Model):
    dealershipID = models.ForeignKey('background.Dealership', on_delete=models.PROTECT)
    salespersonID = models.ForeignKey('background.employee', on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "#"+ str(self.id) + " | " + str(self.dealershipID).title() + " via: " + str(self.salespersonID)

    def get_absolute_url(self):
        return reverse("inventory:detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("inventory:update", kwargs={"id": self.id})

    def get_order_form_children(self):
        return self.order_set.all()

    def get_order_form_total(self):
        children = self.get_order_form_children()
        total = 0
        for child in children:
            total = total + ((1 - child.discount) * child.price * child.quantity)
        return total

class order(models.Model):
    order_formID = models.ForeignKey(order_form, on_delete=models.PROTECT)
    productID = models.ForeignKey('background.product', on_delete=models.PROTECT)
    discount = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=0)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    
    def list(self):
        return self.id
    
    def __str__(self):
        return "#"+ str(self.id) + " | " + str(self.productID)

    def get_absolute_url(self):
        return self.order_formID.get_absolute_url()

    def save(self, *args, **kwargs):
        self.price = self.productID.price
        super(order, self).save(*args, **kwargs)