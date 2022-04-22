from typing import Union
from uuid import uuid4

from django.db import models

from categories.models import Category
from manufacturers.models import Manufacturer
from parameters.models import ListParameter, NumericParameter, Parameter
from specifications.models import Specification


class Component(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='components'
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name='components', null=True
    )
    specification = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name='components', null=True
    )
    numeric_parameters = models.ManyToManyField(
        Parameter,
        related_name='components_with_numeric_params',
        through=NumericParameter,
    )
    list_parameters = models.ManyToManyField(
        Parameter, related_name='components_with_list_params', through=ListParameter
    )

    @property
    def parameters(self) -> list[Union[NumericParameter, ListParameter]]:
        return list(self.listparameter_set.all()) + list(
            self.numericparameter_set.all()
        )
