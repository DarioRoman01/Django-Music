"""POST endpoints test cases."""

# Rest Framework
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

# Models
from apps.music.models import (
    Song,
    Artist,
    Album,
    Playlist
)
from apps.users.models import User

class POSTRequestsAPITestCase(APITestCase):
    """
    POST requests API test case, verify that all
    POST requests succed and the permissions work fine
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test12', email='p@mlh.io', password='test123', is_artist=True)
        self.user.save()

        self.artist = Artist.objects.create(artist_name='freddie testcase', user=self.user)
        self.artist.save()

        self.album = Album.objects.create(
            id=1,
            title='awesome album',
            artist=self.artist,
            release_date='2007-10-25 14:30:59',
        )
        self.album.save()

        self.song = Song.objects.create(
            title='Awesome song',
            release_date='2006-10-25 14:30:59',
            artist=self.artist
        )
        self.song.save()

        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_request_success(self):
        """Verify request succed."""
        url = '/albums/{}/addSong/'.format(self.album.id)
        song_name = self.song.title
        request = self.client.post(url, data={'song_name': song_name})
        self.assertEqual(request.status_code,status.HTTP_200_OK)