"""Albums Models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic
from apps.music.models import Song, Artist

class Album(DjangoMusic):
    """Album model."""

    title = models.CharField(max_length=50)
    songs = models.ManyToManyField(Song, related_name='a_songs')
    cover_image = models.ImageField(upload_to='covers/')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def set_cover_images(self):
        """
        Set his cover image to all the songs related
        with the album
        """
        image = self.cover_image
        songs_list = list(self.songs.all())
        for song in songs_list:
            song.cover_image = image
