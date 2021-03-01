"""Artist serializers."""

# Rest framework
from rest_framework import serializers

# Models
from apps.music.models import Artist

class ArtistModelSerializer(serializers.ModelSerializer):
    """Artist model serializer."""

    class Meta:
        """Meta class."""
        model = Artist
        fields = ('artist_name', 'picture')


class CreateArtistSerializer(serializers.Serializer):
    artist_name =  serializers.CharField(max_length=60)
    picture = serializers.ImageField(required=False)

    def create(self, data):
        user = self.context['user']
        artist = Artist.objects.create(user=user, **data)
        return artist
        