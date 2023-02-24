from django.urls import path

from .views import *

urlpatterns = [
    # Records
    path('flight_schedule', flight_schedule, name='flight_schedule'),
    path('dockings', dockings, name='dockings'),
    path('arrival_schedule', arrival_schedule, name='arrival_schedule'),
    path('departure_schedule', departure_schedule, name='departure_schedule'),
    path('search_records', search_records, name='search_records'),
    path('create_docking', create_docking, name='create_docking'),
    path('create_docking_fids/<str:iata>', create_docking_fids, name='create_docking_fids'),
    path('create_undocking/<int:pk>', create_undocking, name='create_undocking'),
    path('create_nodocking', create_nodocking, name='create_nodocking'),
    path('update_record/<int:pk>/', update_record, name='update_record'),
]