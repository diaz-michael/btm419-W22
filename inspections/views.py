from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# from itertools import product

from .models import inspection
from .forms import inspectionForm

# Create your views here.
def index(request):
    """The home page for Inspections."""
    return render(request, 'inspections/index.html')

@login_required
def inspections_all(request):

    inspections = inspection.objects.all().select_related('claimID').select_related('claimID__warrantyID').select_related('claimID__warrantyID__customerID').select_related('claimID__warrantyID__dealershipID').order_by("-scheduledDate")

    context = {'inspections':inspections}
    return render(request, 'inspections/inspections_table.html', context)

@login_required
def inspection_detail_view(request, id=None):
    obj = get_object_or_404(inspection, id=id) 
    context = {
        "inspection": obj
    }
    return render(request, "inspections/detail.html", context) 

@login_required
def inspection_update_view(request, id=None):
    obj = get_object_or_404(inspection.objects.select_related('claimID').select_related('claimID__warrantyID').select_related('claimID__warrantyID__customerID'), id=id)
    form = inspectionForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    
    if form.is_valid():
        ins = form.save(commit=False)
        messages.success(request, "Inspection updated successfully!")
        ins.save()
        # formset.save()
    return render(request, "inspections/create-update.html", context) 

def inspection_create_view(request):
    form = inspectionForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        ins = form.save(commit=False)
        ins.save()
        return redirect(ins.get_absolute_url())
    return render(request, "inspections/create-update.html", context)
    




