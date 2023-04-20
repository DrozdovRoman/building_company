from django.urls import path

from . import views
from .views import EquipmentTypeView, EngineeringPositionView
from .views import ObjectTypeView, CustomerView, EmployeeView, ConstructionView
from .views import RegionView, SpecializationView, BrigadeView
from .views import BrigadeEmployeeView, EquipmentConstructionTypeView
from .views import BuildingView

urlpatterns = [
    path('', views.index, name='index'),
    path('entity/', views.entity, name='entity'),

    path('equipment-type/',
         EquipmentTypeView.as_view(),
         name='equipment_type'),

    path('equipment-constructuion/',
         EquipmentConstructionTypeView.as_view(),
         name='equipment_construction'),

    path('engineering-position/',
         EngineeringPositionView.as_view(),
         name='engineering-position'),

    path('specialization/',
         SpecializationView.as_view(),
         name='specialization'),

    path('object-type/',
         ObjectTypeView.as_view(),
         name='object_type'),

    path('customer/',
         CustomerView.as_view(),
         name='customer'),

    path('employee/',
         EmployeeView.as_view(),
         name='employee'),

    path('construction/',
         ConstructionView.as_view(),
         name='construction'),

    path('region/',
         RegionView.as_view(),
         name='region'),

    path('brigade/',
         BrigadeView.as_view(),
         name='brigade'),

    path('brigade-employee/',
         BrigadeEmployeeView.as_view(),
         name='brigade_employee'),

    path('building/',
         BuildingView.as_view(),
         name='building'),
]
