from django.contrib import admin

from .models import Dealership, Customer, Product, Employee

admin.site.register(Dealership)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Employee)