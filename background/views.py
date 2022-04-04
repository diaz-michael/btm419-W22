from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.db.models import Count

from django.db.models.functions import Coalesce

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
            customers = Customer.objects.all().annotate(inspection_count=Coalesce(Count('warranty__claim__inspection'),0))
            header = "Customer List"
            table_css_id = "table_db"
        else:
            customers = Customer.objects.filter(email = request.user.email).annotate(inspection_count=Coalesce(Count('warranty__claim__inspection'),0))
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