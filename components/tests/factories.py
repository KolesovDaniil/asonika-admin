from typing import Any

import factory

from categories.tests.factories import CategoryFactory
from manufacturers.tests.factories import ManufacturerFactory
from parameters.models import ParameterTypes
from parameters.tests.factories import ParameterFactory
from specifications.tests.factories import SpecificationFactory

from ..models import Component


class ComponentFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    category = factory.SubFactory(CategoryFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)
    specification = factory.SubFactory(SpecificationFactory)

    class Meta:
        model = Component

    @factory.post_generation
    def add_numeric_parameters_values(self, *args: Any, **kwargs: Any):
        numeric_parameters = ParameterFactory.create_batch(
            size=3, type=ParameterTypes.FLOAT
        )
        self.category.parameters.add(*numeric_parameters)
        for parameter in numeric_parameters:
            self.numericparameter_set.create(parameter=parameter, value=0)

    @factory.post_generation
    def add_list_parameters_values(self, create, extracted, **kwargs):
        list_parameters = ParameterFactory.create_batch(
            size=3, type=ParameterTypes.LIST
        )
        self.category.parameters.add(*list_parameters)
        for parameter in list_parameters:
            self.listparameter_set.create(
                parameter=parameter, value=['test_value', 'test_value']
            )
