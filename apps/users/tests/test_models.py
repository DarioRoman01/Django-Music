"""Users models tests."""

# Django
from django.test import TestCase

# Models
from apps.users.models import User

class TestUserModel(TestCase):
    """User model test case."""

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            username='dummyname',
            first_name='jorge',
            last_name='villalobos'
        )

    def test_user(self):
        user = self.user
        self.assertIsNotNone(user)