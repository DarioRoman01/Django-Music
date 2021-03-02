"""Music apps custom filters."""

# Rest framework
from rest_framework.filters import SearchFilter


class FilterArtistByFollow(SearchFilter):
    """Filter the query to return only the followed artist."""

    def get_search_fields(self, view, request):
        """ Check if followed is in query params."""
        if request.query_params.get('followed'):
            return ['__all__']

    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user followed artists"""
        return request.user.followed_artists.all()

class FilterPlaylistByFollow(SearchFilter):
    """Filter the query to return only the followed playlist."""

    def get_search_fields(self, view, request):
        """ Check if followed is in query params."""
        if request.query_params.get('followed'):
            return ['__all__']

    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user followed playlists"""
        return request.user.followed_playlist.all()

class FilterSongsByLike(SearchFilter):
    """Filter songs by user liked songs."""

    def get_search_fields(self, view, request):
        """ Check if liked is in query params."""
        if request.query_params.get('liked'):
            return ['__all__']
        
    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user liked songs"""
        return request.user.liked_songs.all()

class FilterAlbumsByLike(SearchFilter):
    """Filter albums by users liked albums."""
    
    def get_search_fields(self, view, request):
        """ Check if liked is in query params."""
        if request.query_params.get('liked'):
            return ['__all__']
            
    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user liked albums"""
        return request.user.liked_albums.all()