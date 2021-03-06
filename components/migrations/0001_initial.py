# Generated by Django 3.2.4 on 2022-04-22 07:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_rename_paramtocategorysettings_categoryparameterssettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='categories.category')),
            ],
        ),
    ]
