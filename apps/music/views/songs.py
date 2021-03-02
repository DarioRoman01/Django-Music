"""Songs views"""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsSongOwner, IsArtist

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.music.filters import FilterSongsByLike

# Serializers
from apps.music.serializers import (
    CreateSongSerializer,
    SongModelSeriaizer,
    ArtistModelSerializer
)

# Models
from apps.music.models import Song

class SongViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Songs View set."""
    
    serializer_class = SongModelSeriaizer
    lookup_field = 'title'
    lookup_url_kwarg = 'title'

    # Filter
    filter_backends = (SearchFilter, OrderingFilter, FilterSongsByLike)
    search_fields = ('title', 'artist', 'release_date', 'liked')
    ordering_fields = ('title', 'artist', 'release_date', 'likes')

    def dispatch(self, request, *args, **kwargs):
        """Verify that album exists if id in the url"""
        if 'title' in self.kwargs:
            self.song = get_object_or_404(Song, title=self.kwargs['title'])
            return super(SongViewSet, self).dispatch(request, *args, **kwargs)
        else:
            return super(SongViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action == 'createSong':
            permissions.append(IsArtist)

        return [p() for p in permissions]

    def get_object(self):
        return get_object_or_404(Song, title=self.kwargs['title'])

    def get_queryset(self):
        """Assing querys based on actions."""
        query = Song.objects.all()
        if self.action == 'retrieve':
            return query.get(title=self.kwargs['title'])

        return query

    
    @action(detail=False, methods=['POST'])
    def createSong(self, request):
        """Handle the creation of songs."""
        
        serializer = CreateSongSerializer(
            context={'artist': request.user.artist},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        song = serializer.save()

        data = SongModelSeriaizer(song).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def toggleLike(self, request, title):
        """toggle like endpoint handle likes to the album."""
        song = self.song
        user = request.user

        # Check if the user already liked the song to perform unlike action
        if user.liked_songs.filter(id=song.id).exists():
            user.liked_songs.remove(song)
            song.likes -= 1
            song.save()
            
        # Else perform like action
        else:
            user.liked_songs.add(song)
            song.likes += 1
            song.save()

        data = SongModelSeriaizer(song).data

        return Response(data, status=status.HTTP_200_OK) 