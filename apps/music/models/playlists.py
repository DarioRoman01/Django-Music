"""Albums Models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.music.models import Song


class Playlist(DjangoMusic):
    """Playlist model."""

    title = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, related_name='p_songs')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title