
from django.urls import path
from . import project_views, station_views

urlpatterns = [
    # Home 
    path('', project_views.home, name='home'),
    # Project-related URL patterns
    path('create-project/', project_views.create_project, name='create_project'),
    path('check-project/', project_views.check_project_name, name='check_project_name'),
    path('delete-project/<int:project_id>/', project_views.delete_project, name='delete_project'),

    # Station-related URL patterns
    path('stations/<int:project_id>/', station_views.stations, name='stations'),
    path('upload_config/<int:project_id>/', station_views.upload_config, name='upload_config'),
    path('delete_station/<int:station_id>/', station_views.delete_station, name='delete_station'),
    path('delete_stations/<int:project_id>/', station_views.delete_stations, name='delete_stations'),
    path('station/<int:station_id>/', station_views.view_station, name='view_station'),
]