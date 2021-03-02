"""Artists models."""

# Django
from django.db import models

# Models
from apps.users.models import User
from apps.utils import DjangoMusic

class Artist(DjangoMusic):
    """Artist model. acts like a profile for aritsts users."""

    artist_name = models.CharField(max_length=60)
    picture = models.ImageField(upload_to='artist/') 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, related_name='following', symmetrical=False)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.artist_name
