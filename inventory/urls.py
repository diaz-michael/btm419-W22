from django.urls import path

from .views import (
    order_form_list_view,
    order_form_detail_view,
    order_form_create_view,
    order_form_update_view,
    order_form_start_view
)

app_name='inventory'

urlpatterns = [
    path("", order_form_list_view, name='list'),
    path("create/", order_form_create_view, name='create'),
    path("<int:id>/edit/", order_form_update_view, name='update'),
    path("<int:id>/", order_form_detail_view, name='detail'),
    path("<int:id>/start/", order_form_start_view, name='start'),
]