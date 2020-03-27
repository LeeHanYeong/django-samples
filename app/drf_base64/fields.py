from django.forms import ImageField
from drf_extra_fields.fields import Base64FieldMixin, Base64ImageField, Base64FileField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField


class Base64WithFilenameFieldMixin(Base64FieldMixin):
    INVALID_OBJECT = 'Must be an object containing keys "file_name" and "base64_data"'
    INVALID_DATA = ''
    INVALID_FILE_NAME = 'The file name is incorrect. It should have the form "<name>.<extension>"'
    ALLOW_ALL_EXTENSIONS = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.help_text is None:
            self.help_text = 'An object containing keys `file_name` and `base64_data`'

    def to_internal_value(self, obj):
        if obj in (None, ''):
            return obj

        if not all(key in obj for key in ('file_name', 'base64_data')):
            if self.parent.instance:
                # If an empty value or null is not passed, returns the existing value
                if obj:
                    origin_name = getattr(self.parent.instance, self.source).name
                    return origin_name
                else:
                    return None
            else:
                raise ValidationError(self.INVALID_OBJECT)

        try:
            self.name, self.ext = obj['file_name'].rsplit('.', 1)
        except ValueError:
            raise ValidationError(self.INVALID_FILE_NAME)

        if self.ext not in self.ALLOWED_TYPES and self.ALLOW_ALL_EXTENSIONS:
            self.ALLOWED_TYPES.append(self.ext)

        base64_data = obj['base64_data']
        return super().to_internal_value(base64_data)

    def get_file_name(self, decoded_file):
        return self.name

    def get_file_extension(self, filename, decoded_file):
        return self.ext


class Base64WithFilenameImageField(Base64WithFilenameFieldMixin, Base64ImageField, ImageField):
    ALLOW_ALL_EXTENSIONS = True


class Base64WithFilenameFileField(Base64WithFilenameFieldMixin, Base64FileField, FileField):
    ALLOW_ALL_EXTENSIONS = True
