import factory

from ..models import MeasurementGroup, MeasurementGroupForParameter, MeasurementUnit


class MeasurementGroupFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    description = factory.Faker('text')

    class Meta:
        model = MeasurementGroup


class MeasurementUnitFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    multiplier = 1
    min_value = -100
    max_value = 100
    group = factory.SubFactory(MeasurementGroupFactory)

    class Meta:
        model = MeasurementUnit


class MeasurementGroupForParameterFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    parameter_name = factory.Faker('slug')
    model_name = factory.Faker('slug')
    measurement_group = factory.SubFactory(MeasurementGroupFactory)

    class Meta:
        model = MeasurementGroupForParameter
