from asyncio.windows_events import NULL
from itertools import count
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render
from inventory.models import order
from inspections.models import inspection
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from django.template.defaulttags import register

def is_valid_queryparam(dictionary, name, param):
    if param != '' and param is not None:
        dictionary[name] = param
        return True
    else:
        dictionary[name] = ''
        return False
    
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



def inspection_status_view(request):
    "The Inspection page"    
    inspection_sc_list = inspection.objects.filter(status = 'Sc')
    sc_list = ["Scheduled",len(inspection_sc_list)]
    inspection_cm_list = inspection.objects.filter(status = 'Cm')
    cm_list = ["Cancelled",len(inspection_cm_list)]
    inspection_ex_list = inspection.objects.filter(status = 'Ex')
    ex_list = ["Expired",len(inspection_ex_list)]
    inspection_status_list = [sc_list,cm_list,ex_list]
    inspection_list = inspection.objects.all().select_related('claimID').select_related('claimID__warrantyID').select_related('claimID__warrantyID__customerID').select_related('claimID__warrantyID__dealershipID').order_by("-scheduledDate")
    print(inspection_status_list) 

    x = ["Scheduled", "Cancelled", "Expired"]
    y = [len(inspection_sc_list), len(inspection_cm_list), len(inspection_ex_list)]
    fig, ax = plt.subplots()
    vbar = ax.bar(x, y)
    # Optional: chart title and label axes.
    ax.set_title("Inspection Status", fontsize=24)
    ax.set_xlabel("Status", fontsize=14)
    ax.set_ylabel("Number of Inspection", fontsize=14)
    ax.bar_label(vbar,fmt="%.2f")



    # Create a bytes buffer for saving image
    figbuffer = BytesIO()
    plt.savefig(figbuffer, format='png', dpi=300)
    image_base640=base64.b64encode(figbuffer.getvalue())
    image_base64 = image_base640.decode('utf-8')
    figbuffer.close()    



    return render(request, 'reporting/inspection.html',
    context={'inspection_status_list': inspection_status_list,'inspection_list': inspection_list,'image_base64':image_base64})

def inspection_whole_view(request):
    inspection_list = inspection.objects.all()
    return render(request, 'reporting/inspection.html',
    context={'inspection': inspection_list, "title": "inspection"})

def insFilterView(request):

    qs = inspection.objects.all().select_related('claimID').select_related('claimID__warrantyID').select_related('claimID__warrantyID__customerID').select_related('claimID__warrantyID__dealershipID').order_by("-scheduledDate")
    status_options_list = inspection.STATUS_CHOICES
    status_options = [x[1] for x in status_options_list]    

    name_contains_query = request.GET.get('name_contains')
    makemodel_query = request.GET.get('makemodel')
    yearMin_query = request.GET.get('yearMin')
    yearMax_query = request.GET.get('yearMax')
    dateMin_query = request.GET.get('dateMin')
    dateMax_query = request.GET.get('dateMax')
    status_query = request.GET.get('status')
    # print(status_options_list)
    status_query_code = [item[0] for item in status_options_list if item[1] == status_query]
    # print(status_query_code)

    values = {}

    if is_valid_queryparam(values, 'name', name_contains_query):
        qs = qs.filter(Q(claimID__warrantyID__customerID__first_name__icontains=name_contains_query)
            | Q(claimID__warrantyID__customerID__last_name__icontains=name_contains_query)
            ).distinct()

    if is_valid_queryparam(values, 'makemodel', makemodel_query):
        qs = qs.filter(Q(make__icontains=makemodel_query)
                       | Q(model__icontains=makemodel_query)
                       ).distinct()
        
    if is_valid_queryparam(values, 'yearMin', yearMin_query):
        qs = qs.filter(year__gte=yearMin_query)
        values['yearMin'] = yearMin_query
        
    if is_valid_queryparam(values, 'yearMax', yearMax_query):
        qs = qs.filter(year__lte=yearMax_query)
    
    if is_valid_queryparam(values, 'dateMin', dateMin_query):
        qs = qs.filter(scheduledDate__gte=dateMin_query)

    if is_valid_queryparam(values, 'dateMax', dateMax_query):
        qs = qs.filter(scheduledDate__lte=dateMax_query)
        
    if is_valid_queryparam(values, 'status', status_query) and status_query != "Choose...":
        qs = qs.filter(status=status_query_code[0])

    counts = qs.values('status').annotate(cnt=Count('id')).order_by('status')
    for entry in counts:
        for option in status_options_list:
            if entry['status'] == option[0]:
                        entry['status'] = option[1]

    
    x = status_options
    y = [entry['cnt'] for entry in counts]
    fig, ax = plt.subplots()
    vbar = ax.bar(x, y)
    # Optional: chart title and label axes.
    ax.set_title("Inspection Status", fontsize=24)
    ax.set_xlabel("Status", fontsize=14)
    ax.set_ylabel("Number of Inspection", fontsize=14)
    ax.bar_label(vbar,fmt="%.2f")

    # Create a bytes buffer for saving image
    figbuffer = BytesIO()
    plt.savefig(figbuffer, format='png', dpi=300)
    image_base640=base64.b64encode(figbuffer.getvalue())
    image_base64 = image_base640.decode('utf-8')
    figbuffer.close() 

    # print(values)

    context = {
        'queryset': qs,
        'status_options': status_options,
        'counts': counts,
        'chart': image_base64,
        'filtervalues': values,
    }
    return render(request, "reporting/partials/inspection_filter.html", context)
    


