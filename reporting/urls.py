from django.urls import path
from . import views
##from c3prototype import reporting

app_name = 'reporting'

urlpatterns = [

    path('', views.index, name='index'),
    path('inventory', views.inventory, name='inventory'),
    path('inspection', views.inspection_view, name='inspection')
]
