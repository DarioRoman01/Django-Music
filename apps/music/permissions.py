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
        return request.user.is_artist

class IsArtistOwner(BasePermission):
    """Allow access only to users who are artist.
    and are owners of the artist profile"""

    def has_permission(self, request, view):
        return view.artist.user == request.user 
   
class IsAlbumOwner(BasePermission):
    """Allow access to the artist that own the album."""

    def has_permission(self, request, view):
        if request.user.artist:
            return view.album.artist == request.user.artist
        else:
            return False
    
class IsSongOwner(BasePermission):
    """Allow access to the artist that own the song."""

    def has_permission(self, request, view):
        if request.user.artist:
            return view.song.artist == request.user.artist
        else:
            return False 

class IsPlaylistOwner(BasePermission):
    """Allow access only to the owner to the playlist."""

    def has_permission(self, request, view):
        playlist = view.playlist
        return request.user == playlist.user