"""Songs serializers."""

# Rest framework
from rest_framework import serializers

# Models
from apps.music.models import Song

# Serializers
from apps.music.serializers import ArtistModelSerializer

class SongModelSeriaizer(serializers.ModelSerializer):
    """Song model serializer."""

    artist = ArtistModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Song
        fields = (
            'title',
            'cover_image',
            'song_file',
            'release_date',
            'like',
            'artist'
        )

class CreateSongSerializer(serializers.Serializer):
    """Create song serializer."""

    title = serializers.CharField(max_length=50)
    cover_image = serializers.ImageField(required=False)
    song_file = serializers.FileField(required=True)
    release_date = serializers.DateTimeField()

    def create(self, data):
        """Hadnle song creation."""
        artist = self.context['artist']
        song = Song.objects.create(artist=artist, **data)
        return song