from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Project, Station
from .utils import extract_station_info, extract_fail_code_data

def stations(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stations = Station.objects.filter(project=project)
    return render(request, 'core/station.html', {'stations': stations, 'project': project})

def delete_stations(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        Station.objects.filter(project=project).delete()
        return redirect('stations', project_id=project_id)
    return render(request, 'core/delete_stations.html', {'project': project})

def delete_station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    project_id = station.project.id
    station.delete()
    return redirect('stations', project_id=project_id)

def view_station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    return render(request, 'core/station_detail.html', {'station': station})

def upload_config(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        config_file = request.FILES.get('config_file')

        if config_file and config_file.name.endswith('.xlsm'):
            # Extract station info from the uploaded file
            station_info_list = extract_station_info(config_file)

            # Save each station information to the database
            for station_name, station_description in station_info_list:
                Station.objects.get_or_create(
                    project=project,
                    name=station_name,
                    defaults={'description': station_description}
                )

            # Only extract fail code data if station_info_list has valid data
            if station_info_list:
                fail_code_data_list = extract_fail_code_data(config_file)

                # Process the fail code data as needed
                for fail_code_description in fail_code_data_list:
                    # Here you can save to the database or perform any actions needed
                    pass  # Replace with your saving logic

            return redirect('stations', project_id=project.id)
        else:
            return HttpResponse('Invalid file type', status=400)

    return render(request, 'core/upload_config.html', {'project_id': project_id})