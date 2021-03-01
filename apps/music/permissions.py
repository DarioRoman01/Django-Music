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

    def has_permission(self, request, view):
        return view.artist.user == request.user 
   
    

class IsAlbumOwner(BasePermission):
    """Allow access to the artist that own the album."""

    def has_permission(self, request, view):
        album = view.album
        artist = Artist.objects.get(user=request.user)
        if not artist:
            return False
        else:
            return album.artist == artist
    

class IsSongOwner(BasePermission):
    """Allow access to the artist that own the song."""

    def has_permission(self, request, view):
        song = view.song
        artist = Artist.objects.get(user=request.user)
        if not artist:
            return False
        else:
            return song.artist == artist
    

class IsPlaylistOwner(BasePermission):
    """Allow access only to the owner to the playlist."""

    def has_permission(self, request, view):
        playlist = view.playlist
        return request.user == playlist.user


   