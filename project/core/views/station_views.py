from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project, Station, Actuator

def station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    fail_codes = station.failcodes.all()
    return render(request, 'core/station/index.html', {'fail_codes': fail_codes, 'station': station})

def actuators(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    actuators = Actuator.objects.filter(station=station)
    return render(request, 'core/station/actuators.html', {'actuators': actuators, 'station': station})
