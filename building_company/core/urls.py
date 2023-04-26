from django.urls import path

from . import views
from .views import EquipmentTypeView, EngineeringPositionView
from .views import ObjectTypeView, CustomerView, EmployeeView, ConstructionView
from .views import RegionView, SpecializationView, BrigadeView
from .views import BrigadeEmployeeView, EquipmentConstructionTypeView
from .views import BuildingView, ContractView, QualityView
from .views import ObjectQualityView, TechnologyView, MaterialView
from .views import ObjectTechnologyView, TechnologyMaterialView
from .views import EquipmentBuildingView

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

    path('contract/',
         ContractView.as_view(),
         name='contract'),

    path('quality/',
         QualityView.as_view(),
         name='quality'),

    path('object-quality/',
         ObjectQualityView.as_view(),
         name='object_quality'),

    path('technology/',
         TechnologyView.as_view(),
         name='technology'),

    path('material/',
         MaterialView.as_view(),
         name='material'),

    path('object-technology/',
         ObjectTechnologyView.as_view(),
         name='object_technology'),

    path('technology-material/',
         TechnologyMaterialView.as_view(),
         name='technology_material'),

    path('equipment-building/',
         EquipmentBuildingView.as_view(),
         name='equipment_building'),
]
