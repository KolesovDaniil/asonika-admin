# Generated by Django 3.2.4 on 2022-01-19 20:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('specification_file', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=256, null=True)),
            ],
            options={
                'db_table': 'specifications',
            },
        ),
    ]