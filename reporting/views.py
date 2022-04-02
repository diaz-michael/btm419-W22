from contextvars import Context
from itertools import product
from multiprocessing import context
from django.shortcuts import render
from inventory.models import order
from inspections.models import inspection
from io import BytesIO
import matplotlib.pyplot as plt
import base64


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
    inspection_list = inspection.objects.all()
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


