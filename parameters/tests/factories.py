import factory

from measurements.tests.factories import MeasurementGroupFactory

from ..models import Parameter, ParameterTypes


class ParameterFactory(factory.django.DjangoModelFactory):
    type = ParameterTypes.FLOAT
    name = factory.Faker('slug')
    measurement_group = factory.SubFactory(MeasurementGroupFactory)

    class Meta:
        model = Parameter
