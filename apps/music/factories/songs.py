"""Songs Factory."""

# Factory
import factory
from apps.music.factories import ArtistFactory

class SongFactory(factory.django.DjangoModelFactory):
    """Song model factory."""

    title = factory.Faker('cryptocurrency_name')
    song_file = factory.Faker('file_name')
    artist = factory.SubFactory(ArtistFactory)

    class Meta:
        model = 'music.Song'