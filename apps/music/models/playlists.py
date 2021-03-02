"""Albums Models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.music.models import Song
from apps.users.models import User

class Playlist(DjangoMusic):
    """Playlist model."""

    title = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, related_name='p_songs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, related_name='follows', symmetrical=False)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title