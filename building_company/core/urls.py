from django.urls import path

from . import views
from .views import EquipmentTypeView

urlpatterns = [
    path('', views.index, name='index'),
    path('entity/', views.entity, name='entity'),
    path('equipment_type/', EquipmentTypeView.as_view(), name='equipment_type')
]
