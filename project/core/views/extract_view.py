from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Project, Station, Failcode, Actuator, ActuatorMember
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..utils import extract_station_info, extract_fail_codes,extract_actuators
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
    

# project/core/views/extract_view.py

# project/core/views/extract_view.py

def extract_actuators_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    file_path = request.session.get('uploaded_file_path')
    
    if file_path:
        with default_storage.open(file_path, 'rb') as config_file:
            # Extract actuator information (this will return a dict with sheet names as keys and lists of actuator data as values)
            station_info = extract_actuators(config_file)

            # Loop through each station's data and store the actuator info
            for station_name, actuators in station_info.items():
                # Ensure the station exists in the database (or create if it doesn't exist)
                station = Station.objects.get_or_create(project=project, name=station_name)[0]
                
                # First, create or update the Actuator entries in the database
                for actuator_data in actuators:
                    actuator_id = actuator_data.get('actuator_id', '')

                    # Create or update the Actuator entry in the database
                    Actuator.objects.update_or_create(
                        station=station,
                        actuator_id=actuator_id,
                    )

            # Loop again to create ActuatorMember entries
            for station_name, actuators in station_info.items():
                station = Station.objects.get(project=project, name=station_name)
                for actuator_data in actuators:
                    actuator_id = actuator_data.get('actuator_id', '')
                    actuator = Actuator.objects.get(station=station, actuator_id=actuator_id)

                    # Create ActuatorMember for each actuator
                    ActuatorMember.objects.update_or_create(
                        actuator=actuator,
                        index=actuator_data.get('index', ''),
                        defaults={
                            'name': actuator_data.get('name', ''),
                            'data_type': actuator_data.get('data_type', ''),
                            'prefix': actuator_data.get('prefix', ''),
                            'actuator_output': actuator_data.get('actuator_output', ''),
                            'output_description': actuator_data.get('output_description', ''),
                            'actuator_input': actuator_data.get('actuator_input', ''),
                            'input_description': actuator_data.get('input_description', ''),
                            'alm_0': actuator_data.get('alm_0', ''),
                            'alm_1': actuator_data.get('alm_1', ''),
                            'alm_0_description_language_1': actuator_data.get('alm_0_description_language_1', ''),
                            'alm_0_description_language_2': actuator_data.get('alm_0_description_language_2', ''),
                            'alm_0_description_language_3': actuator_data.get('alm_0_description_language_3', ''),
                            'alm_1_description_language_1': actuator_data.get('alm_1_description_language_1', ''),
                            'alm_2_description_language_2': actuator_data.get('alm_2_description_language_2', ''),
                            'alm_3_description_language_3': actuator_data.get('alm_3_description_language_3', ''),
                            'alm_0_procedure': actuator_data.get('alm_0_procedure', ''),
                            'alm_1_procedure': actuator_data.get('alm_1_procedure', ''),
                            'alm_0_bad': actuator_data.get('alm_0_bad', ''),
                            'alm_1_bad': actuator_data.get('alm_1_bad', ''),
                            'alm_0_cause': actuator_data.get('alm_0_cause', ''),
                            'alm_1_cause': actuator_data.get('alm_1_cause', ''),
                            'alm_0_action': actuator_data.get('alm_0_action', ''),
                            'alm_1_action': actuator_data.get('alm_1_action', ''),
                        }
                    )

        return render(request, 'core/extractconfig/extract_page.html', {
            'project_id': project_id,
            'successActuator': 'Actuators extracted and stored successfully.'
        })
    else:
        return HttpResponse('No file uploaded', status=400)