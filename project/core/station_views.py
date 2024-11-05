from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Project, Station, Failcode
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
    failcodes = Failcode.objects.filter(station=station)
    return render(request, 'core/station_detail.html', {'station': station, 'failcodes': failcodes})

def upload_config(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        config_file = request.FILES.get('config_file')

        if config_file and config_file.name.endswith('.xlsm'):
            # Extract station info from the uploaded file
            station_info_dict = extract_station_info(config_file)

            # Save each station information to the database
            for station_name, df in station_info_dict.items():
                station_description = str(df.iloc[2, 1])  # Ensure the value is a string
                station, created = Station.objects.get_or_create(
                    project=project,
                    name=station_name,
                    defaults={'description': station_description}
                )

                # Extract fail code data for each station
                fail_code_data_list = extract_fail_code_data(df)

                # Save each fail code data to the database
                for fail_code_id, fail_code_description in fail_code_data_list:
                    Failcode.objects.get_or_create(
                        station=station,
                        failcodeID=fail_code_id[:10],  # Assuming the failcodeID is the first 10 characters
                        defaults={'description': fail_code_description}
                    )

            return render(request, 'core/upload_config.html', {
                'project_id': project_id,
                'success': 'Config file uploaded successfully.'
            })
        else:
            return HttpResponse('Invalid file type', status=400)

    return render(request, 'core/upload_config.html', {'project_id': project_id})