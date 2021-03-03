"""Test artist endpoints."""

# Factory
from apps.music.factories import ArtistFactory
from apps.users.factories import UserFactory
from rest_framework.authtoken.models import Token

# Rest framewrork
from rest_framework.test import APITestCase
from rest_framework import status

class ArtistsAPITestCase(APITestCase):
    """Artist API test case."""

    def setUp(self):
        """Test case setup."""

        self.user = UserFactory()
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

        self.artist = ArtistFactory()
        self.artist2 = ArtistFactory()
        self.artist3 = ArtistFactory()
        self.artist4 = ArtistFactory()

    def test_follow_artist_and_filter_by_follow(self):

        # Test follow endpoint 
        url = '/artists/{}/follow/'.format(self.artist.name)
        request = self.client.post(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['name'], self.artist.name)
        self.assertEqual(request.data['followers'], 1)

        # Test filter artists by follow
        url = '/artists/?followed=followed'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 1)
        self.assertEqual(request.data['results'][0]['name'], self.artist.name)


    def test_get_artists(self):
        # Test that all artist are list correctly
        url = '/artists/'
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 4)

        # Test get artist by name
        url = '/artists/{}/'.format(self.artist2.name)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['name'], self.artist2.name)

        





    



