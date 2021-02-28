"""Albums test cases."""

# Django
from django.test import TestCase

# Models
from apps.users.models import User
from apps.music.models import (
    Artist, 
    Song,
    Album
)

class AlbumTestCase(TestCase):
    """Album Test case."""

    def setUp(self):
        self.user = User.objects.create_user(username='test12', email='p@mlh.io', password='test123')
        self.user.save()
        self.artist = Artist.objects.create(artist_name='freddie testcase', user=self.user)
        self.artist.save()

        self.song = Song.objects.create(
            title='Awesome song',
            release_date='2006-10-25 14:30:59',
            artist=self.artist
        )
        self.song.save()

        self.album = Album.objects.create(
            title='awesome album',
            artist=self.artist,
            release_date='2007-10-25 14:30:59',
        )
        self.album.save()


    def test_artist(self):
        self.assertIsNotNone(self.album and self.artist)
        self.assertEqual(self.album.artist, self.artist)

    def test_add_song(self):
        album = self.album
        album.songs.add(self.song)
        album_songs = list(album.songs.all())
        self.assertIsNotNone(album_songs)
        self.assertEqual(album_songs[0], self.song)