from typing import Iterable

import factory

from parameters.tests.factories import ParameterFactory

from ..models import Category, ParamToCategorySettings


class CategoryFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    description = factory.Faker('text')

    class Meta:
        model = Category

    @factory.post_generation
    def with_parameters(self, create, extracted, **kwargs):
        if not extracted:
            return

        if isinstance(extracted, Iterable):
            for parameter in extracted:
                self.parameters.add(parameter)
        else:
            self.parameters.add(ParameterFactory.create())


class ParamToCategorySettingsFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    parameter = factory.SubFactory(ParameterFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = ParamToCategorySettings
