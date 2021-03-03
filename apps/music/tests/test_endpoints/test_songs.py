"""Test songs endpoints."""

# Rest framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

# Factory
from apps.music.factories import ArtistFactory, SongFactory
from apps.users.factories import UserFactory

# Utils
from datetime import datetime

class SongAPITestCase(APITestCase):
    """Song API test case."""

    def setUp(self):
        """Test case set up."""

        self.song = SongFactory()
        self.song2 = SongFactory()
        for i in range(3):
            SongFactory()

        self.artist = ArtistFactory()
        self.artist_token = Token.objects.create(user=self.artist.user)

        self.user = UserFactory()
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    
    def test_create_song(self):
        # Verify that song is created normally
        url = '/songs/createSong/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.artist_token}')
        request = self.client.post(url, data = {"title": "TestSong", "release_date": datetime.now()})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['title'], 'TestSong')

    def test_like_songs_and_filter_by_like(self):

        # Test like to song
        url = '/songs/{}/toggleLike/'.format(self.song.title)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], self.song.title)
        self.assertEqual(request.data['likes'], 1)

        # Test filter by like should return the song liked before this request
        url = '/songs/?liked=liked'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 1)
        self.assertEqual(request.data['results'][0]['title'], self.song.title)

        # Test that all songs are listed
        url = '/songs/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 5)

    def test_fail_requests(self):

        # Test create song without artist status 
        url = '/songs/createSong/'
        request = self.client.post(url, data = {"title": "TestSong", "release_date": datetime.now()})
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        # Test bad request
        url = '/songs/createSong/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.artist_token}')
        request = self.client.post(url, data={})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        # Test get songs without authorization header
        url = '/songs/'
        self.client.credentials()
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)




        
