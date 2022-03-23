from itertools import product
from django.shortcuts import render
from inventory.models import order
from inspections.models import inspection
# Create your views here.
def index(request):
    """The home page for Reporting."""
    return render(request, 'reporting/index.html')


def inventory(request):
    """The reporting page"""
    inventory_list = order.objects.all()
    print(inventory_list)
    return render(request, 'reporting/inventory.html',
    context = {'inventory_list': list(inventory_list), "title": "Inventory"})



def inspection_view(request):
    "The Inspection page"
    inspection_list = inspection.objects.all()
    print(inspection_list[1])
    return render(request, 'reporting/inspection.html',
    context = {'inspection_list': list(inspection_list), "title": "Inspection"})
