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
        self.user_artist = User.objects.create_user(username='test12', email='p@mlh.io', password='test123', is_artist=True)
        self.artist_token = Token.objects.create(user=self.user_artist).key
        self.user_artist.save()

        self.artist = Artist.objects.create(artist_name='freddie testcase', user=self.user_artist)
        self.artist.save()

        self.album = Album.objects.create(
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

        self.user_client = User.objects.create_user(username='12test', email='j@mlh.io', password='test123', is_artist=False)
        self.user_token = Token.objects.create(user=self.user_client)
        

    def test_request_success(self):
        """Verify request succed."""
        url = '/albums/{}/addSong/'.format(self.album.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.artist_token}')

        request = self.client.post(url, data={'song_name': self.song.title})
        self.assertEqual(request.status_code,status.HTTP_200_OK)

    def test_unauthorized_request(self):
        """Test is artist permission."""

        url = '/albums/createAlbum/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.post(url,
            data={
                "title": 'song uwu',
                "release_date": "2007-10-25 14:30:59"
            }
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


    def test_like_to_song(self):
        """Verify that toggle like to song works."""
        url = '/songs/{}/toggleLike/'.format(self.song.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['likes'], 1)

    def test_like_album(self):
        """Verify that toggle like to album works."""
        url = '/albums/{}/toggleLike/'.format(self.song.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['likes'], 1)

    def test_fail_like(self):
        """Test toggle like without authorization."""
        url = '/albums/{}/toggleLike/'.format(self.song.id)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follow_artist(self):
        """Test follow artist endpoint."""
        url = '/artists/{}/follow/'.format(self.artist.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['followers'], 1)

    def test_fail_follow(self):
        """Verify is authenticated permission."""
        url = '/artists/{}/follow/'.format(self.artist.id)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)