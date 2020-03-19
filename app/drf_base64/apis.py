from rest_framework import viewsets

from .models import SampleBase64ImageModel
from .serializers import SampleBase64ImageSerializer


class SampleBase64ImageViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64ImageModel.objects.all()
    serializer_class = SampleBase64ImageSerializer
