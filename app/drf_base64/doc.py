from collections import OrderedDict

from drf_extra_fields.fields import Base64FieldMixin
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import FieldInspector, SwaggerAutoSchema, NotHandled
from drf_yasg.renderers import ReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.fields import ImageField, FileField

from drf_base64.fields import Base64WithFilenameFieldMixin

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


class Base64ImageFieldInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        if issubclass(type(obj), Base64WithFilenameFieldMixin):
            result['example'] = {
                'file_name': 'pby.jpg',
                'base64_data': 'aHR0cHM6Ly9naXRodWIuY29tL2xlZWhhbnllb25n',
            }
        elif issubclass(type(obj), Base64FieldMixin):
            result['example'] = 'aHR0cHM6Ly9naXRodWIuY29tL2xlZWhhbnllb25n'
            if issubclass(type(obj), ImageField):
                result['description'] = 'Base64 encoded image file string'
            elif issubclass(type(obj), FileField):
                result['description'] = 'Base64 encoded file string'
        return result

    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        SwaggerType, ChildSwaggerType = self._get_partial_types(field, swagger_object_type, use_references, **kwargs)

        if issubclass(type(field), Base64WithFilenameFieldMixin):
            properties = OrderedDict()
            properties['file_name'] = openapi.Schema(
                type=openapi.TYPE_STRING, description=r'Uploaded file name with the form **`<name>.<extension>`**')
            properties['base64_data'] = openapi.Schema(
                type=openapi.TYPE_STRING, description='Base64 encoded file string')
            result = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties,
            )
            return result
        elif issubclass(type(field), Base64FieldMixin):
            result = SwaggerType(type=openapi.TYPE_STRING, format=openapi.FORMAT_BASE64)
            return result

        return NotHandled


class CustomSchema(SwaggerAutoSchema):
    field_inspectors = [Base64ImageFieldInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS
