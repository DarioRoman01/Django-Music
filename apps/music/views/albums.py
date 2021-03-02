"""Album views."""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsAlbumOwner, IsArtist
from apps.music.filters import FilterAlbumsByLike

# Serializers
from apps.music.serializers import (
    CreateAlbumSerializer,
    AlbumModelSerializer,
    AddSongSerializer,
    SongModelSeriaizer,
    ArtistModelSerializer
)

# Models
from apps.music.models import Album, Artist

class AlbumViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """Album view set."""

    serializer_class = AlbumModelSerializer
    lookup_field = 'title'
    lookup_url_kwarg = 'title'

    # Filter
    filter_backends = (SearchFilter, OrderingFilter, FilterAlbumsByLike)
    search_fields = ('title', 'release_date', 'liked')
    ordering_fields = ('title', 'release_date', 'likes')

    def dispatch(self, request, *args, **kwargs):
        """Verify that album exists if id in the url"""
        if 'title' in self.kwargs:
            self.album = get_object_or_404(Album, title=self.kwargs['title'])
            return super(AlbumViewSet, self).dispatch(request, *args, **kwargs)
        else:
            return super(AlbumViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action == 'createAlbum':
            permissions.append(IsArtist)

        elif self.action == 'addSong':
            permissions.append(IsAlbumOwner)
            permissions.append(IsArtist)

        return [p() for p in permissions]

    def get_object(self):
        """Return specific album."""
        return get_object_or_404(Album, title=self.kwargs['title'])

    def get_queryset(self):
        """Assing querys based on actions."""

        query = Album.objects.all()

        if self.action in ['retrieve', 'addSong']:
            return query.get(title=self.kwargs['title'])

        return query

    @action(detail=False, methods=['POST'])
    def createAlbum(self, request):
        """Handle album creation."""
        artist = Artist.objects.get(user=request.user)
        serializer = CreateAlbumSerializer(
            context={'artist': artist},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        album = serializer.save()

        data = AlbumModelSerializer(album).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def addSong(self, request, title):
        """Handle adding songs to the album instance."""
        album_context = self.album
        serializer = AddSongSerializer(
            context={'album': album_context},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        data = AlbumModelSerializer(album).data

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def toggleLike(self, request, title):
        """toggle like endpoint handle likes to the album."""
        album = self.album
        user = request.user

        # Check if the user already like the album to perform unlike action
        if user.liked_albums.filter(id=album.id).exists():
            user.liked_albums.remove(album)
            album.likes -= 1
            album.save()
        
        # else perform like action
        else:
            user.liked_albums.add(album)
            album.likes += 1
            album.save()

        data = AlbumModelSerializer(album).data

        return Response(data, status=status.HTTP_200_OK)
            