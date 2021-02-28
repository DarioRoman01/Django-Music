"""Artists test case."""

# Django
from django.test import TestCase

# models
from apps.music.models import Artist
from apps.users.models import User

class ArtistTestCase(TestCase):
    """Artist test case."""

    def setUp(self):
        self.user = User.objects.create_user(username='test12', email='p@mlh.io', password='test123')
        self.user.save()
        self.artist = Artist.objects.create(artist_name='freddie testcase', user=self.user)
        self.artist.save()

    def tearDown(self):
        self.user.delete()
        self.artist.delete()

    def test_relation(self):
        self.assertIsNotNone(self.artist and self.user)
        self.assertEqual(self.artist.user, self.user)
