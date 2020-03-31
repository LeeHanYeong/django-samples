from rest_framework import viewsets

from .models import SampleBase64ImageModel, SampleBase64FileModel, SampleParentModel
from .serializers import (
    SampleBase64ImageSerializer, SampleBase64FileSerializer,
    SampleBase64WithFilenameImageSerializer, SampleBase64WithFilenameFileSerializer,
    SampleParentFilenameImageSerializer)


class SampleBase64ImageViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64ImageModel.objects.all()
    serializer_class = SampleBase64ImageSerializer


class SampleBase64FileViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64FileModel.objects.all()
    serializer_class = SampleBase64FileSerializer


class SampleBase64WithFilenameImageViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64ImageModel.objects.all()
    serializer_class = SampleBase64WithFilenameImageSerializer


class SampleBase64WithFilenameFileViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64FileModel.objects.all()
    serializer_class = SampleBase64WithFilenameFileSerializer


class SampleParentWithFilenameImageViewSet(viewsets.ModelViewSet):
    queryset = SampleParentModel.objects.all()
    serializer_class = SampleParentFilenameImageSerializer
