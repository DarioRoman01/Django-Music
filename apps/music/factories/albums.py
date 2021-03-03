"""Albums Factory."""

# Factory
import factory
from apps.music.factories import ArtistFactory

class AlbumFactory(factory.django.DjangoModelFactory):
    """Album model factory."""

    title = factory.Faker('cryptocurrency_name')
    cover_image = factory.Faker('file_name')
    artist = factory.SubFactory(ArtistFactory)
    release_date = factory.Faker('date_time_this_century')

    class Meta:
        model = 'music.Album'