import factory

from ..models import Specification


class SpecificationFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Faker('slug')
    specification_file = factory.Faker('slug')

    class Meta:
        model = Specification
