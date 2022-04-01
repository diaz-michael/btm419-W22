from operator import concat
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm
from .forms import RegisterForm
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import *
from inspections.models import claim, inspection
from .decorators import *

def home(request):
    if not request.user.is_authenticated:
        return render(request = request,
                    template_name='background/home.html',
                    context = {"products":Product.objects.all})
    else:
        if request.user.is_staff:
            customers = Customer.objects.all()
            header = "Customer List"
            table_css_id = "tableDB"
        else:
            customers = Customer.objects.filter(email = request.user.email) 
            customer = customers.first().first_name
            header = "Welcome " + customer + "!"
            table_css_id = "tableOne"
        context = {
            "customers": customers,
            "header": header,
            "table_css_id": table_css_id,
        }
        return render(request, 'background/customers.html', context)

def customerinfo(request, pk):
    customer = Customer.objects.get(id=pk)
    warranties = customer.warranty_set.all()
    claims = [claim
                for warranty in warranties
                for claim in warranty.claim_set.all()]
    inspections = [inspection
                    for claim in claims
                    for inspection in claim.inspection_set.all()]
    context = {'customer':customer, 'warranties':warranties, 'claims':claims, 'inspections':inspections}
    return render(request, 'background/customerinfo.html', context)

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "background/register.html", {"form":form})