from uuid import uuid4

from django.db import models

from asonika_admin.utils import ChoicesEnum
from measurements.models import MeasurementGroup


class ParameterTypes(int, ChoicesEnum):
    LIST = 1, 'Список'
    FLOAT = 2, 'Число с плавающей точкой'


class Parameter(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    type = models.PositiveIntegerField(choices=ParameterTypes.choices())
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    measurement_group = models.ForeignKey(
        MeasurementGroup, on_delete=models.CASCADE, related_name='parameters'
    )

    def __str__(self) -> str:
        return f'{self.name}'
