""" Sonngs models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.users.models import User
from apps.music.models import Artist

class Song(DjangoMusic):
    """Song model."""

    title = models.CharField(max_length=50)
    cover_image = models.ImageField()
    song_file = models.FileField(upload_to='songs/')
    release_date = models.DateTimeField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='s_like')
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title