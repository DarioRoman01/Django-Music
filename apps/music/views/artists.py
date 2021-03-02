"""Artists views."""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsArtistOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from apps.music.serializers import (
    CreateArtistSerializer,
    ArtistModelSerializer,
    ArtistVerificationSerializer
)

# Models 
from apps.music.models import Artist, Album

# Serializers
from apps.music.serializers import (
    ArtistModelSerializer,
    AlbumModelSerializer
)

class ArtistViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Artist view set."""

    serializer_class = ArtistModelSerializer

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('artist_name',)
    ordering_fields = ('artist_name', 'followers')

    def dispatch(self, request, *args, **kwargs):
        """Verify that artist exists if id in the url"""
        if 'pk' in self.kwargs:
            self.artist = get_object_or_404(Artist, pk=self.kwargs['pk'])
            return super(ArtistViewSet, self).dispatch(request, *args, **kwargs)
        else:
            return super(ArtistViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assing permissions based on actions."""
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update']:
            permissions.append(IsArtistOwner)

        return [p() for p in permissions]

    def get_object(self):
        """return aritst instance."""
        return get_object_or_404(Artist, pk=self.kwargs['pk'])

    def get_queryset(self):
        """Assing querys based on actions."""
        query = Artist.objects.all()

        if self.action == ['update', 'partial_update', 'retrieve', 'follow']:
            return query.get(pk=self.kwargs['pk'])

        return query

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """Handle artist registration."""
        serializer = CreateArtistSerializer(context={'user': request.user} ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'Message': 'Your are one step close to become an artist'}

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def verifyArtist(self, request):
        """Handle artist verification."""
        serializer = ArtistVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = serializer.save()
        data = {
            'artist': ArtistModelSerializer(artist).data,
            'message': 'Congratulations now you are an artist, now go and share your talent'
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk):
        """Follow endpoint, handle how users follows an artist."""
        artist = self.artist

        if artist.follow.filter(id=request.user.id).exists():
            artist.follow.remove(request.user)
            artist.followers -= 1
            artist.save()

        else:
            artist.follow.add(request.user)
            artist.followers += 1
            artist.save()

        data = ArtistModelSerializer(artist).data

        return Response(data, status=status.HTTP_200_OK) 