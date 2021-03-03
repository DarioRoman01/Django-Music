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
        """Filter query based on user followed artists or playlists."""
        search_fields = self.get_search_fields(view, request)

        if not search_fields:
            return queryset

        if view.name == 'PlaylistViewSet':
            queryset = request.user.followed_playlist.all()

        elif view.name == 'ArtistViewSet':
            queryset = request.user.followed_artists.all()

        return queryset


class FilterByLike(SearchFilter):
    """Filter songs by user liked songs or albums."""

    def get_search_fields(self, view, request):
        """ Check if liked is in query params."""
        if request.query_params.get('liked'):
            return ['__all__']

    def filter_queryset(self, request, queryset, view):
        """Filter query based on user followed albums or songs."""
        search_fields = self.get_search_fields(view, request)

        if not search_fields:
            return queryset

        if view.name == 'SongViewSet':
            queryset = request.user.liked_songs.all()
        elif view.name == 'AlbumViewSet':
            queryset = request.user.liked_albums.all()

        return queryset