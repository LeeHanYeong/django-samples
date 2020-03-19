from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register(r'', apis.SampleBase64ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
