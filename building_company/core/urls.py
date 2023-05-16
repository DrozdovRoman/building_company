from django.urls import path, include
from . import views
from .views import EquipmentTypeView, EngineeringPositionView
from .views import ObjectTypeView, CustomerView, EmployeeView, ConstructionView
from .views import RegionView, SpecializationView, BrigadeView
from .views import BrigadeEmployeeView, EquipmentConstructionTypeView
from .views import BuildingView, ContractView, QualityView
from .views import ObjectQualityView, TechnologyView, MaterialView
from .views import ObjectTechnologyView, TechnologyMaterialView
from .views import EquipmentBuildingView, TimetableView, EstimationView
from .views import EstimationFactView

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('', views.index, name='index'),
    path('entity/', views.entities, name='entity'),
    path('tasks/', views.tasks, name='tasks'),
    path('task-1/', views.task1, name='task_1'),
    path('task-2/', views.task2, name='task_2'),
    path('task-2/result/', views.task2_result, name='task_2_result'),
    path('task-3/', views.task3, name='task_3'),
    path('task-3/result/', views.task3_result, name='task_3_result'),
    path('task-4/', views.task4, name='task_4'),
    path('task-4/result/', views.task4_result, name='task_4_result'),
    path('task-5/', views.task5, name='task_5'),
    path('task-5/result/', views.task5_result, name='task_5_result'),
    path('task-6/', views.task6, name='task_6'),
    path('task-6/result/', views.task6_result, name='task_6_result'),
    path('task-7/', views.task7, name='task_7'),
    path('task-7/result/', views.task7_result, name='task_7_result'),
    path('task-8/', views.task8, name='task_8'),
    path('task-8/result/', views.task8_result, name='task_8_result'),
    path('task-9/', views.task9, name='task_9'),
    path('task-9/result/', views.task9_result, name='task_9_result'),
    path('task-10/', views.task10, name='task_10'),
    path('task-10/result/', views.task10_result, name='task_10_result'),
    path('task-11/', views.task11, name='task_11'),
    path('task-11/result/', views.task11_result, name='task_11_result'),
    path('task-12/', views.task12, name='task_12'),
    path('task-12/result/', views.task12_result, name='task_12_result'),
    path('task-13/', views.task13, name='task_13'),
    path('task-13/result/', views.task13_result, name='task_13_result'),

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

    path('timetable/',
         TimetableView.as_view(),
         name='timetable'),

    path('estimation/',
         EstimationView.as_view(),
         name='estimation'),

    path('estimation-fact/',
         EstimationFactView.as_view(),
         name='estimation_fact'),
]
