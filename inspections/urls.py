from django.urls import path
from . import views

app_name = 'inspections'

urlpatterns = [
    path('all', views.inspections_all, name="all"),
    path("<int:id>/", views.inspection_detail_view, name='detail'),
    path("create/", views.inspection_create_view, name='create'),
    path("<int:id>/edit/", views.inspection_update_view, name='update'),
]