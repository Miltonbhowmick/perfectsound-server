from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import *

app_name = "music"

router = DefaultRouter()
router.register(r"tracks", PublicTrackViewset, basename="tracks")
router.register(r"artists", PublicArtistViewset, basename="artists")
router.register(r"albums", PublicAlbumViewset, basename="albums")
router.register(r"playlists", PublicPlaylistViewset, basename="playlists")
router.register(r"genre", PublicGenreViewset, basename="genre")

urlpatterns = [path("public/", include(router.urls))]
