"""Music apps custom filters."""

# Rest framework
from rest_framework.filters import SearchFilter

# Models
from apps.music.models import (
    Artist,
    Album,
    Song,
    Playlist
)
from apps.users.models import User


class FilterArtistByFollow(SearchFilter):
    """Filter the query to return only the followed artist."""

    def get_search_fields(self, view, request):
        if request.query_params.get('followed'):
            queryset = User.followed_artists.all()
            return queryset 

        return super().get_search_fields(view, request)

class FilterPlaylistByFollow(SearchFilter):
    """Filter the query to return only the followed playlist."""

    def get_search_fields(self, view, request):
        if request.query_params.get('followed'):
            queryset = User.followed_playlist.all()
            return queryset

        return super().get_search_fields(view, request)

class FilterSongsByLike(SearchFilter):
    """Filter songs by user liked songs."""

    def get_search_fields(self, view, request):
        if request.query_params.get('liked'):
            queryset = User.liked_songs.all()
            return queryset
        return super().get_search_fields(view, request)

class FilterAlbumsByLike(SearchFilter):
    """Filter albums by users liked albums."""
    
    def get_search_fields(self, view, request):
        if request.query_params.get('liked'):
            queryset = User.liked_albums.all()
            return queryset
            
        return super().get_search_fields(view, request)