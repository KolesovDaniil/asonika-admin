from uuid import uuid4

from django.db import models

from asonika_admin.utils import ChoicesEnum


class ParameterTypes(int, ChoicesEnum):
    LIST = 1, 'Список'
    FLOAT = 2, 'Число с плавающей точкой'


class Parameter(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    type = models.PositiveIntegerField(choices=ParameterTypes.choices())
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    parameters = models.ManyToManyField(Parameter, related_name='categories')

    def __str__(self) -> str:
        return f'{self.name}'
