
from django.urls import path
from .views import extract_view, project_views, station_views, stations_views, fail_code_views

urlpatterns = [
    # Home 
    path('', project_views.home, name='home'),
    # Project-related URL patterns
    path('create-project/', project_views.create_project, name='create_project'),
    path('check-project/', project_views.check_project_name, name='check_project_name'),
    path('delete-project/<int:project_id>/', project_views.delete_project, name='delete_project'),

    # Stations-related URL patterns
    path('stations/<int:project_id>/', stations_views.stations, name='stations'),
    path('delete_station/<int:station_id>/', stations_views.delete_station, name='delete_station'),
    path('delete_stations/<int:project_id>/', stations_views.delete_stations, name='delete_stations'),
    path('extract_config_file/<int:project_id>/', stations_views.extract_config_file, name='extract_config_file'),
    
    # Station-Specific-related URL patterns
    path('station/<int:station_id>/', station_views.station, name='station'),
    path('actuators/<int:station_id>/', station_views.actuators, name='actuators'),
    
    # Fail Code -related URL patterns
    path('fail_codes/<int:station_id>/', fail_code_views.fail_codes, name='fail_codes'),
    path('delete_fail_code/<int:fail_code_id>/', fail_code_views.delete_fail_code, name='delete_fail_code'),
    path('delete_fail_codes/<int:station_id>/', fail_code_views.delete_fail_codes, name='delete_fail_codes'),

    
    # extract-related URL patterns
    path('extract_page/<int:project_id>/', extract_view.extract_page, name='extract_page'),
    path('upload_config/<int:project_id>/', extract_view.upload_config, name='upload_config'),
    path('extract_fail_codes/<int:project_id>/', extract_view.extract_fail_codes_view, name='extract_fail_codes'),
    path('extract_actuators/<int:project_id>/', extract_view.extract_actuators_view, name='extract_actuators'),
    
]