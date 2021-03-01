"""Users urls."""

# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# views
from apps.music import views

# Router init
router = DefaultRouter()

# Registering view sets
router.register(r'artists', views.ArtistViewSet, basename='artist')
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(r'albums', views.AlbumViewSet, basename='album')
router.register(r'songs', views.SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls))
]