# Generated by Django 3.2.4 on 2022-03-16 11:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.PositiveIntegerField(choices=[(1, 'Список'), (2, 'Число с плавающей точкой')])),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]