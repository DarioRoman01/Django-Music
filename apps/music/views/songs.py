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
    SongModelSeriaizer,
    ArtistModelSerializer
)

# Models
from apps.music.models import Song

class SongViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Songs View set."""
    
    serializer_class = SongModelSeriaizer

    def dispatch(self, request, *args, **kwargs):
        """Verify that album exists."""
        pk = self.kwargs['pk']
        self.song = get_object_or_404(Song, pk=pk)
        return super(SongViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action == 'createSong':
            permissions.append(IsArtist)

        return [p() for p in permissions]

    def get_object(self):
        return get_object_or_404(Song, pk=self.kwargs['pk'])

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

    @action(detail=True, methods=['POST'])
    def toggleLike(self, request, pk):
        """toggle like endpoint handle likes to the album."""
        song = self.song

        # Check if the user already liked the song to perform unlike action
        if song.like.filter(id=request.user.id).exists():
            song.like.remove(request.user)
            song.likes -= 1
            song.save()
            
        # Else perform like action
        else:
            song.like.add(request.user)
            song.likes += 1
            song.save()

        data = SongModelSeriaizer(song).data

        return Response(data, status=status.HTTP_200_OK) 