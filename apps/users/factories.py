"""Users factory."""

# Factory
import factory

# Rest framework
from rest_framework.authtoken.models import Token


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory."""

    username = factory.Sequence(lambda n: 'user%d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)
    is_artist = False
    
    class Meta:
        model = 'users.User'
