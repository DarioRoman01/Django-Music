"""Albums endpoints test case."""

# Rest framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

# Factory
import factory
from apps.music.factories import AlbumFactory, ArtistFactory, SongFactory
from apps.users.factories import UserFactory

# utils
from datetime import datetime

class AlbumAPITestCase(APITestCase):
    """Album API test case."""

    def setUp(self):
        self.album = AlbumFactory()
        self.album2 = AlbumFactory()
        for i in range(3):
            AlbumFactory()

        self.artist = ArtistFactory()
        self.artist_token = Token.objects.create(user=self.artist.user)
        self.song = SongFactory(artist=self.artist, release_date=datetime.now())

        self.user = UserFactory()
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        

    def test_create_album_and_add_song(self):
        """Test that the album is created fine."""

        # Test album creation
        url = '/albums/createAlbum/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.artist_token}')
        request = self.client.post(
            url,
            data = {"title": 'OWO', 'release_date': '2007-10-25 14:30:59'}
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['artist']['name'], self.artist.name)

        # test adding a song to the album
        url = '/albums/{}/addSong/'.format('OWO')
        request = self.client.post(url, data={"song_name": self.song.title})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(request.data['songs'])
        self.assertEqual(request.data['songs'][0]['title'], self.song.title)

    def test_like_album_and_filter_by_like(self):

        # Test like endpoint
        url = '/albums/{}/toggleLike/'.format(self.album.title)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], self.album.title)
        self.assertEqual(request.data['likes'], 1)

        # Test filter by like
        url = '/albums/?liked=liked/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 1)
        self.assertEqual(request.data['results'][0]['title'], self.album.title)

        # Test list all albums
        url = '/albums/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 5)

    
    def test_fail_requests(self):

        # Test get albums without token
        url = '/albums/'
        self.client.credentials()
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test create album with normal user status
        url = '/albums/createAlbum/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        request = self.client.post(
            url,
            data = {"title": 'OWO', 'release_date': '2007-10-25 14:30:59'}
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        # test not found error
        url = 'albums/addAlbum/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

        # Test bad request
        url = '/albums/createAlbum/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.artist_token}')
        request = self.client.post(
            url,
            data = {"title": 'SONG'}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)