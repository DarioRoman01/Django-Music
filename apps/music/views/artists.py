"""Artists views."""

# Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.music.permissions import IsArtistOwner

# Serializers
from apps.music.serializers import (
    CreateArtistSerializer,
    ArtistModelSerializer,
    ArtistVerificationSerializer
)

# Models 
from apps.music.models import Artist

class ArtistViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Artist view set."""

    serializer_class = ArtistModelSerializer

    def get_permissions(self):
        """Assing permissions based on actions."""

        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAuthenticated, IsArtistOwner]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    def get_object(self):
        return get_object_or_404(
            Artist,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        query = Artist.objects.all()

        if self.action == ['update', 'partial_update', 'retrieve']:
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
        serializer = ArtistVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = serializer.save()
        data = {
            'artist': ArtistModelSerializer(artist).data,
            'message': 'Congratulations now you are an artist, now go and share your talent'
        }

        return Response(data, status=status.HTTP_200_OK)