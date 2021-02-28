"""Song test cases."""

# Django
from django.test import TestCase

# Models
from apps.users.models import User
from apps.music.models import Artist, Song

# utils
from datetime import datetime

class SongTestCase(TestCase):
    """Song test case."""

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

    def tearDown(self):
        self.user.delete()
        self.artist.delete()
        self.song.delete()

    def test_artist(self):
        self.assertIsNotNone(self.song and self.artist and self.user)
        self.assertEqual(self.song.artist, self.artist)