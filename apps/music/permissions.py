"""Music objects permissions."""

# Rest framework
from rest_framework.permissions import BasePermission

# Models
from apps.music.models import (
    Artist,
    Album,
    Song
)

class IsArtist(BasePermission):
    """Allow access only to users with artist status."""

    def has_permission(self, request, view):
        if request.user.is_artist:
            return True
        else:
            return False

class IsArtistOwner(BasePermission):
    """Allow access only to users who are artist.
    and are owners of the artist profile"""

    def has_object_permission(self, request, view, obj):
        
        try:
            Artist.objects.get(user=request.user)

        except Artist.DoesNotExist:
            return False

        return True

class IsAlbumOwner(BasePermission):
    """Allow access to the artist that own the album."""

    def has_object_permission(self, request, view, obj):
        """Check if the artist own the album."""

        try:
            Album.objects.get(artist=request.user.artist)

        except Album.DoesNotExist:
            return False

        return True

class IsSongOwner(BasePermission):
    """Allow access to the artist that own the song."""

    def has_object_permission(self, request, view, obj):
        """Check if the artist own the song."""
        
        try:
            Song.objects.get(artist=request.user.artist)

        except Song.DoesNotExist:
            return False

        return True



   