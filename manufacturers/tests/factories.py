import factory

from ..models import Manufacturer


class ManufacturerFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    description = factory.Faker('text')

    class Meta:
        model = Manufacturer
