"""GET endpoints test cases."""

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

class GETRequestsAPITestCase(APITestCase):
    """Get request API test case. verify that all get
    requests work fine and how the api perform with bad requests
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

    def test_get_artist_endpoint(self):
        url = '/artists/{}/'.format(self.artist.id)
        request = self.client.get(url)
        import pdb; pdb.set_trace()
        self.assertEqual(request.status_code, status.HTTP_200_OK)