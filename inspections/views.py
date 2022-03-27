from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# from itertools import product

from .models import inspection
from .forms import inspectionForm

# Create your views here.
def index(request):
    """The home page for Inspections."""
    return render(request, 'inspections/index.html')

@login_required
def inspections_all(request):
    """The inpections page"""
    # claim_list = claim.objects.all()
    # inspection_list = inspection.objects.all()
    # warranty_list = warranty.objects.all()
    # customer_list = Customer.objects.all()
    # dealership_list = Dealership.objects.all()

    # context = {'claim_list': list(claim_list), 'inspection_list': (inspection_list),'warranty_list': warranty_list,'customer_list': customer_list,'dealership_list': dealership_list },

    #print(inventory_list)

    inspections = inspection.objects.all().order_by("-scheduledDate")
    # Product.objects.all().filter(sub_category__category_id=category_id).select_related('parent')


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
    obj = get_object_or_404(inspection, id=id)
    form = inspectionForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        ins = form.save(commit=False)
        ins.save()
        # formset.save()
        context['message'] = 'Order saved.'
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
    




