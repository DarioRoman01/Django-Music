""" Sonngs models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.music.models import Artist

class Song(DjangoMusic, models.Model):
    """Song model."""

    title = models.CharField(max_length=50)
    song_file = models.FileField(upload_to='songs/')
    release_date = models.DateTimeField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title