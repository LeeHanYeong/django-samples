from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.renderers import ReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .inspector import Base64ImageFieldInspector

BaseSchemaView = get_schema_view(
    openapi.Info(
        title='DRF Base64 Image/File field',
        default_version='v1',
        description='tBoard API Document',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class ReDocSchemaView(BaseSchemaView):
    renderer_classes = (ReDocRenderer, OpenAPIRenderer)


class CustomSchema(SwaggerAutoSchema):
    field_inspectors = [Base64ImageFieldInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS
