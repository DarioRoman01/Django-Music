"""PLaylist endpoints test case."""

# Rest framework
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

# Factory
from apps.music.factories import PlaylistFactory, SongFactory
from apps.users.factories import UserFactory

class PlaylistAPITestCase(APITestCase):
    """Playlist API test case."""

    def setUp(self):
        """Test case setup."""

        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)

        self.user2 = UserFactory()
        self.token2 = Token.objects.create(user=self.user2)

        self.playlist = PlaylistFactory(user=self.user)
        self.playlist2 = PlaylistFactory()
        for i in range(3):
            PlaylistFactory()

        self.song = SongFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')            

    def test_create_playlist(self):
        """Test create playlist endpoint."""

        url = '/playlists/createPlaylist/'
        request = self.client.post(url, data={'title': 'MyPlaylist'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(request.data['title'], 'MyPlaylist')

    def test_follow_and_filter_by_follow(self):

        # Test follow action over playlist
        url = '/playlists/{}/follow/'.format(self.playlist2.title)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], self.playlist2.title)

        # Test filter playlists by follow
        url = '/playlists/?followed=followed/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 1)
        self.assertEqual(request.data['results'][0]['title'], self.playlist2.title)

    def test_add_song(self):
        url = '/playlists/{}/addSong/'.format(self.playlist.title)
        request = self.client.post(url, data={'song_name': f'{self.song.title}'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], self.playlist.title)
        self.assertEqual(request.data['songs'][0]['title'], self.song.title)

    def test_fail_requests(self):
        
        # Test get without authorization header
        url = '/playlists/'
        self.client.credentials()
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test user try to add songs to other playlists of another user
        url = '/playlists/{}/addSong/'.format(self.playlist.title)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request = self.client.post(url, data={'song_name': f'{self.song.title}'})
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

        # Test bad request
        url = '/playlists/{}/addSong/'.format(self.playlist.title)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        request = self.client.post(url, data={})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

