# Generated by Django 3.2.4 on 2022-05-04 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_change_min_max_values_to_float'),
        ('parameters', '0003_add_constraints_for_numeric_and_list_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='measurement_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='measurements.measurementgroup'),
        ),
    ]
