from django.http import HttpResponse, Http404
from django.conf import settings
import os

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .filters import *


class PublicTrackViewset(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TrackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TrackFilter

    def get_serializer_class(self):
        if self.action == "list":
            return MinimalTrackSerializer
        elif self.action == "retrieve":
            return TrackSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context


class PublicArtistViewset(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ArtistSerializer


class PublicAlbumViewset(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AlbumSerializer


class PublicPlaylistViewset(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlaylistSerializer


class PublicGenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GenreSerializer


def download_audio_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="audio/mpeg")
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(file_path)}"'
            )
            return response
    else:
        raise Http404
