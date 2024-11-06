from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project, Station

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

def extract_config_file(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stations = Station.objects.filter(project=project)
    return render(request, 'core/extractconfig/extract_page.html', {'project': project})

