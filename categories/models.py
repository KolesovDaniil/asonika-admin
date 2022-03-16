from uuid import uuid4

from django.db import models


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class ParamToCategorySettings(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    param_uuid = models.UUIDField()
    category_uuid = models.UUIDField()
    required = models.BooleanField()

    class Meta:
        unique_together = [('param_uuid', 'category_uuid')]
