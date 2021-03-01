"""Songs views"""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsSongOwner, IsArtist

# Serializers
from apps.music.serializers import (
    CreateSongSerializer,
    SongModelSeriaizer
)

# Models
from apps.music.models import Song

class SongViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Songs View set."""
    
    serializer_class = SongModelSeriaizer

    def get_permissions(self):
        """Assing permissions based on actions."""
        if self.action == 'retrieve':
            permissions = [IsAuthenticated]
        elif self.action == 'createSong':
            permissions = [IsAuthenticated, IsArtist]
        return [p() for p in permissions]

    def get_object(self):
        return get_object_or_404(
            Song,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        """Assing querys based on actions."""
        query = Song.objects.all()
        if self.action == 'retrieve':
            return query.get(pk=self.kwargs['pk'])

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
    