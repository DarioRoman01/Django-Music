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
            'artist',
            'songs'
        )

class CreateAlbumSerializer(serializers.Serializer):
    """Create Album serializer."""

    title = serializers.CharField(max_length=50)
    cover_image = serializers.ImageField(required=True),
    release_date = serializers.DateTimeField()

    def create(self, data):
        artist = self.context['artist']
        album = Album.objects.create(artist=artist, **data)
        return album


class AddSongSerializer(serializers.Serializer):
    """Add song serializer, handle adding songs to an album."""

    song_name = serializers.CharField()

    def validate(self, data):
        song_name = data['song_name']
        song = Song.objects.get(song_name)

        if not song:
            raise serializers.ValidationError('Song not found:( ')

        return song

    def create(self, data):
       album = self.context['album']
       song = data['song_name']
       album.songs.add(song)

       return album
