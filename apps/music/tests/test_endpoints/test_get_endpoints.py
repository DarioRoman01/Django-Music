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
        self.artist_user = User.objects.create_user(username='test12', email='p@mlh.io', password='test123', is_artist=True)
        self.artist_user.save()
        self.artist_token = Token.objects.create(user=self.artist_user).key

        self.artist = Artist.objects.create(name='freddie testcase', user=self.artist_user)
        self.artist.save()

        self.album = Album.objects.create(
            id=1,
            title='awesome album',
            artist=self.artist,
            release_date='2007-10-25 14:30:59',
        )
        self.album.save()

        self.song = Song.objects.create(
            title='awaeuwu',
            release_date='2006-10-25 14:30:59',
            artist=self.artist
        )
        self.song.save()

        self.song2 = Song.objects.create(
            title='tesla',
            release_date='2006-10-25 14:30:59',
            artist=self.artist
        )
        self.song2.save()

        self.playlist = Playlist.objects.create(title='awesome playlist', user=self.artist_user)
        self.playlist.save()

        self.user_client = User.objects.create_user(username='12test', email='j@mlh.io', password='test123', is_artist=False)
        self.user_token = Token.objects.create(user=self.user_client)


    def test_get_artist_endpoint(self):
        url = '/artists/{}/'.format(self.artist.name)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_album_endpoint(self):
        url = '/albums/{}/'.format(self.album.title)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_song_endpoint(self):
        url = '/songs/{}/'.format(self.song.title)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_without_authorization(self):
        url = '/songs/{}/'.format(self.song.title)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_artist_by_follow(self):
        url = '/artists/?followed'
        self.user_client.followed_artists.add(self.artist)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_filter_playlist_by_follow(self):
        url = '/playlists/?followed'
        self.user_client.followed_playlist.add(self.playlist)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_filter_songs_by_like(self):
        url = '/songs/?liked'
        self.user_client.liked_songs.add(self.song)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
