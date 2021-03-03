"""Albums serializers."""

# Rest Framework
from rest_framework import serializers

# Models
from apps.music.models import Album, Song

# Serializers
from apps.music.serializers import (
    ArtistModelSerializer,
    SongModelSeriaizer
)

class AlbumModelSerializer(serializers.ModelSerializer):
    """Album Model serializer."""

    artist = ArtistModelSerializer(read_only=True)
    songs = SongModelSeriaizer(read_only=True, many=True)

    class Meta:
        """Meta class."""

        model = Album
        fields = (
            'title',
            'cover_image',
            'release_date',
            'likes',
            'artist',
            'songs'
        )
        read_only_fields = ('likes',)

class CreateAlbumSerializer(serializers.Serializer):
    """Create Album serializer."""

    title = serializers.CharField(max_length=50)
    cover_image = serializers.ImageField(required=False)
    release_date = serializers.DateTimeField()

    def create(self, data):
        """Handle album creation."""
        
        artist = self.context['artist']
        album = Album.objects.create(artist=artist, **data)
        return album


class AddSongSerializer(serializers.Serializer):
    """Add song serializer, handle adding songs to an album."""

    song_name = serializers.CharField()

    def validate(self, data):
        """Validate if the song introduced exists."""
        song_name = data['song_name']

        if Song.objects.filter(title=song_name).exists():
            song = Song.objects.get(title=song_name)
            self.context['song'] = song
            return data
        else:
            raise serializers.ValidationError('Song not found:( ')

      

    def create(self, data):
        """Handle adding the song to an album."""
        album = self.context['album']
        song = self.context['song']
        album.songs.add(song)

        return album
