"""Music apps custom filters."""

# Rest framework
from rest_framework.filters import SearchFilter

class FilterByFollow(SearchFilter):
    """Filter the query to return only the followed playlist or artist."""

    def get_search_fields(self, view, request):
        """ Check if followed is in query params."""
        if request.query_params.get('followed'):
            return ['__all__']

    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user followed playlists or artist"""
        if view.name == 'PlaylistViewSet':
            return request.user.followed_playlist.all()
        else:
            return request.user.followed_artists.all()

class FilterByLike(SearchFilter):
    """Filter songs by user liked songs or albums."""

    def get_search_fields(self, view, request):
        """ Check if liked is in query params."""
        if request.query_params.get('liked'):
            return ['__all__']
        
    def filter_queryset(self, request, queryset, view):
        """return query based on requesting user liked songs or albums"""
        if view.name == 'SongViewSet':
            return request.user.liked_songs.all()
        else:
            return request.user.liked_albums.all()