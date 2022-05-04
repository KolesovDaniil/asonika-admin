from typing import Any
from uuid import uuid4

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
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

    def __hash__(self) -> int:
        return hash(str(self.uuid))


class NumericParameter(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    parameter = models.ForeignKey(
        Parameter, related_name='numeric_parameters', on_delete=models.CASCADE
    )
    component = models.ForeignKey('components.Component', on_delete=models.CASCADE)
    value = models.FloatField(null=True)

    class Meta:
        unique_together = [('parameter', 'component')]

    def __str__(self) -> str:
        return f'NumericParameter: {self.uuid}, value: {self.value}'

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.parameter.type == ParameterTypes.FLOAT:
            raise ValidationError(
                'Numeric parameter must refer to parameter with float type'
            )
        super().save(*args, **kwargs)


class ListParameter(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    parameter = models.ForeignKey(
        Parameter, related_name='list_parameters', on_delete=models.CASCADE
    )
    component = models.ForeignKey('components.Component', on_delete=models.CASCADE)
    value = ArrayField(models.CharField(max_length=256), default=list, null=True)

    class Meta:
        unique_together = [('parameter', 'component')]

    def __str__(self) -> str:
        return f'ListParameter: {self.uuid}, value: {self.value}'

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.parameter.type == ParameterTypes.LIST:
            raise ValidationError(
                'List parameter must refer to parameter with list type'
            )
        super().save(*args, **kwargs)
