"""Users factory."""

# Factory
import factory

# Rest framework
from rest_framework.authtoken.models import Token


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory."""

    username = factory.Faker('first_name_nonbinary')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a: '{}@example.com'.format(a.first_name).lower())

    class Meta:
        model = 'users.User'
