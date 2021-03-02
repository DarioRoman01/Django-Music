"""Artists models."""

# Django
from django.db import models

# Models
from apps.utils import DjangoMusic

class Artist(DjangoMusic):
    """Artist model. acts like a profile for aritsts users."""

    name = models.CharField(max_length=60)
    picture = models.ImageField(upload_to='artist/') 
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    followers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
