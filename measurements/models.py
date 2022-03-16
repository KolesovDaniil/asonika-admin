from uuid import uuid4

from django.conf import settings
from django.db import models


class MeasurementGroup(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=settings.DEFAULT_CHAR_FIELD_LENGTH, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'measurement_group'


class MeasurementUnit(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=settings.DEFAULT_CHAR_FIELD_LENGTH, unique=True)
    multiplier = models.IntegerField()
    min_value = models.BigIntegerField()
    min_is_included = models.BooleanField(default=True)
    max_value = models.BigIntegerField()
    max_is_included = models.BooleanField(default=True)
    group = models.ForeignKey(
        MeasurementGroup, on_delete=models.CASCADE, related_name='units'
    )

    class Meta:
        db_table = 'measurement_unit'
