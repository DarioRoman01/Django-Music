"""Music objects permissions."""

# Rest framework
from rest_framework.permissions import BasePermission

# Models
from apps.music.models import (
    Artist,
    Album,
    Song,
    Playlist
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
        aritst = obj
        if aritst.user == request.user:
            return True
        else:
            return False    
    

class IsAlbumOwner(BasePermission):
    """Allow access to the artist that own the album."""

    def has_object_permission(self, request, view, obj):
        """Check if the artist own the album."""
        album = obj

        if album.artist == request.user.artist:
            return True
        else:
            return False

class IsSongOwner(BasePermission):
    """Allow access to the artist that own the song."""

    def has_object_permission(self, request, view, obj):
        """Check if the artist own the song."""
        song = obj

        if song.artist == request.user.artist:
            return True

        else:
            return False
            
    

class IsPlaylistOwner(BasePermission):
    """Allow access only to the owner to the playlist."""

    def has_object_permission(self, request, view, obj):
        playlist = obj
        if playlist.user == request.user:
            return True
        else:
            return False



   