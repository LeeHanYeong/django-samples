from django.urls import path, include

from drf_base64.doc import ReDocSchemaView

urlpatterns = [
    path('doc/', ReDocSchemaView.as_cached_view(cache_timeout=0), name='schema-redoc'),
    path('drf_base64/', include('drf_base64.urls')),
]
