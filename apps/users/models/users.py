"""Users models."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Models
from apps.utils import DjangoMusic
from apps.music import models as MyModels


class User(DjangoMusic, AbstractUser):
    """User model. Extends from django abstract 
    user model and some extra fields"""

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    picture = models.ImageField(
        'users image',
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries. '
            'Clients are the main type of user.'
        )
    )

    is_artist = models.BooleanField(
        'reviewer',
        default=False,
        help_text='help to distinguish artists from the normal users'
    )

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )

    followed_artists = models.ManyToManyField(
        MyModels.Artist, 
        related_name='followed_aritst',
        symmetrical=False,
        help_text='help to perform querys based on artist that user follows'
    )

    followed_playlist = models.ManyToManyField(
        MyModels.Playlist,
        related_name='followed_playlist',
        symmetrical=False,
        help_text='help to perform querys based on playlist that user follows'
    )

    liked_songs = models.ManyToManyField(
        MyModels.Song,
        related_name='liked_songs',
        symmetrical=False,
        help_text='help to perform querys based on songs the user liked'
    )

    liked_albums = models.ManyToManyField(
        MyModels.Album,
        related_name='liked_albums',
        symmetrical=False,
        help_text='help to perform querys based on albums the user liked'
    )


    def __str__(self):
        return self.username
    
    def get_short_name(self):
        return self.username