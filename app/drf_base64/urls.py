from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register(r'image', apis.SampleBase64ImageViewSet)
router.register(r'file', apis.SampleBase64FileViewSet)
router.register(r'image-name', apis.SampleBase64WithFilenameImageViewSet)
router.register(r'file-name', apis.SampleBase64WithFilenameFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
