"""Albums Models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.users.models import User
from apps.music.models import Song, Artist

class Album(DjangoMusic):
    """Album model."""

    title = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, related_name='a_songs')
    cover_image = models.ImageField(upload_to='covers/')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    like = models.ManyToManyField(User, related_name='a_like')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
