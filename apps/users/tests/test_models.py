"""Users models tests."""

# Django
from django.test import TestCase
from django.contrib.auth import authenticate

# Models
from apps.users.models import User

class UsersTestCase(TestCase):
    """User model test case."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            username='dummyname',
            first_name='jorge',
            last_name='villalobos',
            password='testpassword123',
            is_verified=True,
            is_client=True,
            is_artist=False
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_user(self):
        user = self.user
        self.assertIsNotNone(user)
        self.assertTrue(user.is_verified and user.is_client)
        self.assertFalse(user.is_artist)

    def test_sign_in(self):
        user = authenticate(username='test@test.com', password='testpassword123')
        self.assertTrue((user is not None) and user.is_authenticated)
    
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='testpassword123')
        self.assertFalse(user is not None and user.is_authenticated)
    
    def test_wrong_password(self):
        user = authenticate(username='test@test.com', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)