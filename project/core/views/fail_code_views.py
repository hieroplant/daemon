from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project, Station, Failcode

def fail_codes(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    fail_codes = station.failcodes.all()
    return render(request, 'core/fail_codes.html', {'fail_codes': fail_codes, 'station': station})

def delete_fail_codes(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    if request.method == "POST":
        Failcode.objects.filter(station=station).delete()
        return redirect('fail_codes', station_id=station_id)
    return render(request, 'core/delete_fail_codes.html', {'station': station})

def delete_fail_code(request, fail_code_id):
    fail_code = get_object_or_404(Failcode, id=fail_code_id)
    station_id = fail_code.station.id
    fail_code.delete()
    return redirect('fail_codes', station_id=station_id)