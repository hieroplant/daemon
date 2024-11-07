# Generated by Django 4.2.16 on 2024-11-07 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='Pars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pars_id', models.CharField(max_length=4)),
                ('parameter', models.CharField(max_length=10)),
                ('pars_min', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=10)),
                ('pars_max', models.CharField(max_length=10)),
                ('severity', models.CharField(max_length=10)),
                ('description_language_1', models.CharField(max_length=255)),
                ('description_language_2', models.CharField(max_length=255)),
                ('description_language_3', models.CharField(max_length=255)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pars', to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='Failcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failcodeID', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failcodes', to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=100)),
                ('data_type', models.CharField(max_length=100)),
                ('tag_type', models.CharField(max_length=100)),
                ('tag_reference', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declarations', to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='Actuator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actuator_id', models.CharField(max_length=10, unique=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Actuator', to='core.station')),
            ],
        ),
        migrations.CreateModel(
            name='ActuatorMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('data_type', models.CharField(max_length=50)),
                ('prefix', models.CharField(max_length=20)),
                ('actuator_output', models.CharField(max_length=100)),
                ('output_description', models.CharField(max_length=255)),
                ('actuator_input', models.CharField(max_length=100)),
                ('input_description', models.CharField(max_length=255)),
                ('alm_0', models.CharField(max_length=100)),
                ('alm_1', models.CharField(max_length=100)),
                ('alm_0_description_language_1', models.CharField(max_length=255)),
                ('alm_0_description_language_2', models.CharField(max_length=255)),
                ('alm_0_description_language_3', models.CharField(max_length=255)),
                ('alm_1_description_language_1', models.CharField(max_length=255)),
                ('alm_2_description_language_2', models.CharField(max_length=255)),
                ('alm_3_description_language_3', models.CharField(max_length=255)),
                ('alm_0_procedure', models.CharField(max_length=10)),
                ('alm_1_procedure', models.CharField(max_length=10)),
                ('alm_0_bad', models.CharField(max_length=10)),
                ('alm_1_bad', models.CharField(max_length=10)),
                ('alm_0_cause', models.CharField(max_length=255)),
                ('alm_1_cause', models.CharField(max_length=255)),
                ('alm_0_action', models.CharField(max_length=255)),
                ('alm_1_action', models.CharField(max_length=255)),
                ('actuator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='core.actuator')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.actuatormember')),
            ],
            options={
                'unique_together': {('actuator', 'index')},
            },
        ),
    ]
