"""PLaylists serializers."""

# Rest framework
from rest_framework import serializers

# Models
from apps.music.models import Playlist, Song

# Serializers
from apps.music.serializers import SongModelSeriaizer

class PlaylistModelSerializer(serializers.ModelSerializer):
    """Playlist model serializer."""

    songs = SongModelSeriaizer(read_only=True, many=True)

    class Meta:
        """Meta class."""

        model = Playlist
        fields = ('title', 'songs')


class CreatePlaylistSerializer(serializers.Serializer):
    """Create playlist serializer."""

    title = serializers.CharField(max_length=50)

    def create(self, data):
        user = self.context['user']
        playlist = Playlist.objects.create(user=user, **data)

        return playlist

class AddSongSerializer(serializers.Serializer):
    """
    Add song serializer, handle adding
    songs to a playlist
    """

    song_name = serializers.CharField(max_length=60)

    def validate(self, data):
        song_name = data['song_name']
        song = Song.objects.get(title=song_name)

        if not song:
            raise serializers.ValidationError('Song not found')

        return song

    def create(self, validated_data):
        song = validated_data['song']
        playlist = self.context['playlist']

        playlist.songs.add(song)

        return playlist