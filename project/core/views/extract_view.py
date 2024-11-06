from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project, Station, Failcode
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..utils import extract_station_info,extract_fail_codes
import pandas as pd


def extract_page(request, project_id):
    return render(request, 'core/extractconfig/extract_page.html', {'project_id': project_id})

def upload_config(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        config_file = request.FILES.get('config_file')

        if config_file and config_file.name.endswith('.xlsm'):
            # Save the uploaded file to a temporary location
            file_path = default_storage.save('tmp/' + config_file.name, ContentFile(config_file.read()))
            request.session['uploaded_file_path'] = file_path

            # Extract station info from the uploaded file
            station_info_dict = extract_station_info(config_file)

            # Save each station information to the database
            for station_name, df in station_info_dict.items():
                station_description = str(df.iloc[2, 1])  # Ensure the value is a string
                Station.objects.get_or_create(
                    project=project,
                    name=station_name,
                    defaults={'description': station_description}
                )

            return render(request, 'core/extractconfig/extract_page.html', {
                'project_id': project_id,
                'successConfigFile': 'Config file uploaded successfully.'
            })
        else:
            return HttpResponse('Invalid file type', status=400)

    return render(request, 'core/extractconfig/extract_page.html', {'project_id': project_id})

def extract_fail_codes_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    file_path = request.session.get('uploaded_file_path')
    
    if file_path:
        with default_storage.open(file_path, 'rb') as config_file:
            for station in Station.objects.filter(project=project):
                fail_codes = extract_fail_codes(config_file, sheet_name=station.name)
                for code, description in fail_codes.get(station.name, []):
                    Failcode.objects.get_or_create(station=station, failcodeID=code, defaults={'description': description})
        return render(request, 'core/extractconfig/extract_page.html', {
            'project_id': project_id,
            'successFailCode': 'Fail codes extracted and stored successfully.'
        })
    else:
        return HttpResponse('No file uploaded', status=400)