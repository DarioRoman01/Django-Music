"""Playlist views."""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsPlaylistOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from apps.music.serializers import (
    CreatePlaylistSerializer,
    PlaylistModelSerializer,
    AddToPlaylistSerializer
)

# Models
from apps.music.models import Playlist

class PlaylistViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """Playlist view set."""

    serializer_class = PlaylistModelSerializer

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'followers')
    ordering_fields = ('title', 'followers')

    def dispatch(self, request, *args, **kwargs):
        """Verify that playlist exists if id in the url"""
        if 'pk' in self.kwargs:
            self.playlist = get_object_or_404(Playlist, pk=self.kwargs['pk'])
            return super(PlaylistViewSet, self).dispatch(request, *args, **kwargs)
        else:
            return super(PlaylistViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action == 'addSong':
            permissions.append(IsPlaylistOwner)

        return [p() for p in permissions]

    def get_object(self):
        """Get specific playlist."""
        return get_object_or_404(Playlist, pk=self.kwargs['pk'])

    def get_queryset(self):
        """Assing querys based on actions."""
        query = Playlist.objects.all()
        if self.action in ['retrieve', 'addSong']:
            return query.get(pk=self.kwargs['pk'])

    
    @action(detail=False, methods=['POST'])
    def createPlaylist(self, request):
        """Handle playlist creation."""

        serializer = CreatePlaylistSerializer(
            context={'user': request.user},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        playlist = serializer.save()
        data = PlaylistModelSerializer(playlist).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def addSong(self, request, pk):
        """handle adding song to a playlist."""
        serializer = AddToPlaylistSerializer(
            context={'playlist': self.get_object()},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        playlist = serializer.save()
        data = PlaylistModelSerializer(playlist).data

        return Response(data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'])
    def follow(self, request, pk):
        """Follow endpoint, handle how users follows the playlist."""
        playlist = self.playlist

        # Check if requesting user already follow the playlist
        if playlist.follow.filter(id=request.user.id).exists():
            playlist.follow.remove(request.user)
            playlist.followers -= 1
            playlist.save()
        
        # if user dont follow the playlist is added to the playlist followers.
        else:
            playlist.follow.add(request.user)
            playlist.followers += 1
            playlist.save()

        data = PlaylistModelSerializer(playlist).data

        return Response(data, status=status.HTTP_200_OK)
        