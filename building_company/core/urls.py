from django.urls import path

from . import views
from .views import EquipmentTypeView, PositionTypeView, SpecializationView
from .views import ObjectTypeView, CustomerView, EmployeeView, ConstructionView
from .views import ConstructionEmployeeView, RegionView
urlpatterns = [
    path('', views.index, name='index'),
    path('entity/', views.entity, name='entity'),
    path('equipment-type/',
         EquipmentTypeView.as_view(),
         name='equipment_type'),

    path('position-type/',
         PositionTypeView.as_view(),
         name='position_type'),

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
]
