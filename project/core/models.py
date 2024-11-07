from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

class Station(models.Model):
    project = models.ForeignKey(to=Project, related_name="stations", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

class Failcode(models.Model):
    station = models.ForeignKey(to=Station, related_name="failcodes", on_delete=models.CASCADE)
    failcodeID = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    
class Declaration(models.Model):
    station = models.ForeignKey(to=Station, related_name="declarations", on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    domain = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    tag_type = models.CharField(max_length=100)
    tag_reference = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class Actuator(models.Model):
    station = models.ForeignKey(to=Station, related_name="Actuator", on_delete=models.CASCADE)
    actuator_id = models.CharField(max_length=10)

class ActuatorMember(models.Model):
    actuator = models.ForeignKey(Actuator, related_name='members', on_delete=models.CASCADE)
    index = models.CharField(max_length=50) 
    name = models.CharField(max_length=50)  # Name of the member (e.g., "Dial", "CamDialStop")
    data_type = models.CharField(max_length=50)  # Data type (e.g., "Act_Bin", "Alias")
    prefix = models.CharField(max_length=20)
    actuator_output = models.CharField(max_length=100)
    output_description = models.CharField(max_length=255)
    actuator_input = models.CharField(max_length=100)
    input_description = models.CharField(max_length=255)
    alm_0 = models.CharField(max_length=100)
    alm_1 = models.CharField(max_length=100)
    alm_0_description_language_1 = models.CharField(max_length=255)
    alm_0_description_language_2 = models.CharField(max_length=255)
    alm_0_description_language_3 = models.CharField(max_length=255)
    alm_1_description_language_1 = models.CharField(max_length=255)
    alm_2_description_language_2 = models.CharField(max_length=255)
    alm_3_description_language_3 = models.CharField(max_length=255)
    alm_0_procedure = models.CharField(max_length=10)
    alm_1_procedure = models.CharField(max_length=10)
    alm_0_bad = models.CharField(max_length=10)
    alm_1_bad = models.CharField(max_length=10)
    alm_0_cause = models.CharField(max_length=255)
    alm_1_cause = models.CharField(max_length=255)
    alm_0_action = models.CharField(max_length=255)
    alm_1_action = models.CharField(max_length=255)
    

    
# class Actuator(models.Model):
#     station = models.ForeignKey(to=Station, related_name="atuators", on_delete=models.CASCADE)
#     actuator_id = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     index = models.CharField(max_length=10)
#     data_type = models.CharField(max_length=100)
#     prefix = models.CharField(max_length=20)
#     actuator_output = models.CharField(max_length=100)
#     output_description = models.CharField(max_length=255)
#     actuator_input = models.CharField(max_length=100)
#     input_description = models.CharField(max_length=255)
#     alm_0 = models.CharField(max_length=100)
#     alm_1 = models.CharField(max_length=100)
#     alm_0_description_language_1 = models.CharField(max_length=255)
#     alm_0_description_language_2 = models.CharField(max_length=255)
#     alm_0_description_language_3 = models.CharField(max_length=255)
#     alm_1_description_language_1 = models.CharField(max_length=255)
#     alm_2_description_language_2 = models.CharField(max_length=255)
#     alm_3_description_language_3 = models.CharField(max_length=255)
#     alm_0_procedure = models.CharField(max_length=10)
#     alm_1_procedure = models.CharField(max_length=10)
#     alm_0_bad = models.CharField(max_length=10)
#     alm_1_bad = models.CharField(max_length=10)
#     alm_0_cause = models.CharField(max_length=255)
#     alm_1_cause = models.CharField(max_length=255)
#     alm_0_action = models.CharField(max_length=255)
#     alm_1_action = models.CharField(max_length=255)

class Pars(models.Model):
    station = models.ForeignKey(to=Station, related_name="pars", on_delete=models.CASCADE)
    pars_id = models.CharField(max_length=4)
    parameter = models.CharField(max_length=10)
    pars_min = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    pars_max = models.CharField(max_length=10)
    severity = models.CharField(max_length=10)
    description_language_1 = models.CharField(max_length=255)
    description_language_2 = models.CharField(max_length=255)
    description_language_3 = models.CharField(max_length=255)