"""Playlist factory."""

# factory
import factory
from apps.users.factories import UserFactory

class PlaylistFactory(factory.django.DjangoModelFactory):
    """Playlist model factory."""

    title = factory.Faker('cryptocurrency_name')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'music.Playlist'