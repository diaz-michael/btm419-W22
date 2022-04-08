from django.db.models import Count, Sum, F, FloatField, Avg, Max, Min

from django.db.models import Q, Value
from django.db.models.functions import Concat, Coalesce
from django.shortcuts import render
from inventory.models import order_form
from inspections.models import inspection
from background.models import Product
from io import BytesIO
import matplotlib.pyplot as plt
import base64


def is_valid_queryparam(dictionary, name, param):
    if param != '' and param is not None:
        dictionary[name] = param
        return True
    else:
        dictionary[name] = ''
        return False

#Wedge formating for pie chart
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return('''{p:.2f}%
({v:d})'''.format(p=pct, v=val))
    return my_autopct


# Create your views here.
def index(request):
    """The home page for Reporting."""
    return render(request, 'reporting/index.html')


def inventory(request):
    """The reporting page"""
    qs = order_form.objects.all().prefetch_related('order_set').prefetch_related(
        'order_set__productID').select_related('dealershipID').select_related('salespersonID').order_by('-id')

    # for filter
    product_list = Product.objects.all().values_list('name', flat=True)
    qs = qs.annotate(totalqty=Coalesce(Sum('order__quantity'), 0))
    qs = qs.annotate(totalsum=Coalesce(Sum((1 - F('order__discount')) *
                     F('order__quantity') * F('order__price'), output_field=FloatField()), 0))
    qs = qs.annotate(search_name=Concat(
        'salespersonID__first_name', Value(' '), 'salespersonID__last_name'))

    # get filter selections
    name_contains_query = request.GET.get('name_contains')
    salesperson_contains_query = request.GET.get('salesperson')
    totalMin_query = request.GET.get('totalMin')
    totalMax_query = request.GET.get('totalMax')
    qtyMin_query = request.GET.get('qtyMin')
    qtyMax_query = request.GET.get('qtyMax')
    product_query = request.GET.get('product')
    placedDateMin_query = request.GET.get('placedDateMin')
    placedDateMax_query = request.GET.get('placedDateMax')
    updatedDateMin_query = request.GET.get('updatedDateMin')
    updatedDateMax_query = request.GET.get('updatedDateMax')

    values = {}  # keep filter static

    # filter queryset
    if is_valid_queryparam(values, 'name', name_contains_query):
        qs = qs.filter(dealershipID__dealership__icontains=name_contains_query)

    if is_valid_queryparam(values, 'salesperson', salesperson_contains_query):
        qs = qs.filter(search_name__icontains=salesperson_contains_query)

    if is_valid_queryparam(values, 'totalMin', totalMin_query):
        qs = qs.filter(totalsum__gte=totalMin_query)
    if is_valid_queryparam(values, 'totalMax', totalMax_query):
        qs = qs.filter(totalsum__lte=totalMax_query)
    if is_valid_queryparam(values, 'qtyMin', qtyMin_query):
        qs = qs.filter(totalqty__gte=qtyMin_query)
    if is_valid_queryparam(values, 'qtyMax', qtyMax_query):
        qs = qs.filter(totalqty__lte=qtyMax_query)
    if is_valid_queryparam(values, 'placedDateMin', placedDateMin_query):
        qs = qs.filter(date__gte=placedDateMin_query)
    if is_valid_queryparam(values, 'placedDateMax', placedDateMax_query):
        qs = qs.filter(date__lte=placedDateMax_query)
    if is_valid_queryparam(values, 'updatedDateMin', updatedDateMin_query):
        qs = qs.filter(updated__gte=updatedDateMin_query)
    if is_valid_queryparam(values, 'updatedDateMax', updatedDateMax_query):
        qs = qs.filter(updated__lte=updatedDateMax_query)

    if is_valid_queryparam(values, 'product', product_query) and product_query != "Order includes...":
        qs = qs.filter(id__in=qs.filter(
            order__productID__name__icontains=product_query))

    productcounts = qs.values('order__productID__name').annotate(
        sum=Sum('order__quantity')).order_by('order__productID__name')
    summarytable = qs.aggregate(Avg('totalsum'), Max(
        'totalsum'), Min('totalsum'), Count('id'))

    # make products sold by qty pie chart
    labels = list(
        filter(None, [entry['order__productID__name'] for entry in productcounts]))
    sums = list(filter(None, [entry['sum'] for entry in productcounts]))
    # print(sums)
    fig, ax = plt.subplots()
    ax.pie(sums, labels=labels, autopct=make_autopct(
        sums), pctdistance=0.8, startangle=90)
    ax.axis('equal')
    ax.set_title("Products Sold by Quantity", fontsize=24)

    # Create a bytes buffer for saving image
    figbuffer = BytesIO()
    plt.savefig(figbuffer, format='png', dpi=300, bbox_inches='tight')
    image_base640 = base64.b64encode(figbuffer.getvalue())
    product_image = image_base640.decode('utf-8')
    figbuffer.close()

    context = {
        'inventory_list': qs,
        'filtervalues': values,
        'product_list': product_list,
        'product_image': product_image,
        'summarytable': summarytable
    }
    return render(request, 'reporting/inventory.html', context)


def insFilterView(request):

    qs = inspection.objects.all().select_related('claimID').select_related('claimID__warrantyID').select_related(
        'claimID__warrantyID__customerID').select_related('claimID__warrantyID__dealershipID').order_by("-scheduledDate")
    status_options_list = inspection.STATUS_CHOICES
    status_options = [x[1] for x in status_options_list]

    # get filter selections
    name_contains_query = request.GET.get('name_contains')
    makemodel_query = request.GET.get('makemodel')
    yearMin_query = request.GET.get('yearMin')
    yearMax_query = request.GET.get('yearMax')
    dateMin_query = request.GET.get('dateMin')
    dateMax_query = request.GET.get('dateMax')
    status_query = request.GET.get('status')
    # print(status_options_list)
    status_query_code = [item[0]
                         for item in status_options_list if item[1] == status_query]
    # print(status_query_code)

    values = {}

    # filter queryset
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

    x = [entry['status'] for entry in counts]
    y = [entry['cnt'] for entry in counts]
    fig, ax = plt.subplots()
    vbar = ax.bar(x, y)
    # Optional: chart title and label axes.
    ax.set_title("Inspection Status", fontsize=24)
    ax.set_xlabel("Status", fontsize=14)
    ax.set_ylabel("Number of Inspection", fontsize=14)
    ax.bar_label(vbar, fmt="%.2f")

    # Create a bytes buffer for saving image
    figbuffer = BytesIO()
    plt.savefig(figbuffer, format='png', dpi=300, bbox_inches='tight')
    image_base640 = base64.b64encode(figbuffer.getvalue())
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
    return render(request, "reporting/inspection_filter.html", context)
