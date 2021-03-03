"""Arstist factory."""

# Factory
import factory
from apps.users.factories import UserFactory

class ArtistFactory(factory.django.DjangoModelFactory):
    """Artist model factory."""

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('first_name_nonbinary')

    class Meta:
        model = 'music.Artist'