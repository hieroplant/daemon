# Generated by Django 4.2.16 on 2024-11-07 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actuator',
            name='actuator_id',
            field=models.CharField(max_length=10),
        ),
    ]
