from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entity/', views.entity, name='entity'),
    path('equipment_type/', views.equipment_type, name='equipment_type')
]
