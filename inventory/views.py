from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory  # model form for querysets
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import order_formForm, orderForm
from .models import order_form, order

# via https://github.com/codingforentrepreneurs/Try-Django-3.2


@login_required
def order_form_list_view(request):
    qs = order_form.objects.all().prefetch_related('order_set').select_related(
        'dealershipID').select_related('salespersonID').order_by('-id')

    context = {
        "object_list": qs
    }
    return render(request, "inventory/list.html", context)


@login_required
def order_form_detail_view(request, id=None):
    obj = get_object_or_404(order_form.objects.prefetch_related('order_set').prefetch_related(
        'order_set__productID').select_related('dealershipID').select_related('salespersonID'), id=id)
    context = {
        "object": obj
    }
    return render(request, "inventory/detail.html", context)


@login_required
def order_form_create_view(request):
    form = order_formForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        #obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_start_url())
    return render(request, "inventory/create-update.html", context)


@login_required
def order_form_update_view(request, id=None):
    obj = get_object_or_404(order_form, id=id)
    form = order_formForm(request.POST or None, instance=obj)
    # Formset = modelformset_factory(Model, form=ModelForm, extra=0)
    orderFormset = modelformset_factory(order, form=orderForm, extra=0)
    qs = obj.order_set.all()  # []
    formset = orderFormset(request.POST or None, queryset=qs)
    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        # formset.save()
        for form in formset:
            child = form.save(commit=False)
            child.order_formID = parent
            child.price = child.productID.price
            child.save()
        context['saved'] = True
        messages.success(request, "Order saved successfully!")
    if request.htmx:
        return render(request, "inventory/partials/forms.html", context)
    return render(request, "inventory/create-update.html", context)


@login_required
def order_form_start_view(request, id=None):
    obj = get_object_or_404(order_form, id=id)
    context = {
        "obj": obj
    }
    return render(request, "inventory/start_order.html", context)
