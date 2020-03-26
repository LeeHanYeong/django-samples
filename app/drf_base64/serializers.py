from drf_extra_fields.fields import Base64ImageField, Base64FileField
from rest_framework import serializers

from .fields import Base64WithFilenameImageField, Base64WithFilenameFileField
from .models import SampleBase64ImageModel, SampleBase64FileModel


class SampleBase64ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = SampleBase64ImageModel
        fields = (
            'id',
            'image',
        )


class SampleBase64FileSerializer(serializers.ModelSerializer):
    file = Base64FileField(required=False)

    class Meta:
        model = SampleBase64FileModel
        fields = (
            'id',
            'file',
        )


class SampleBase64WithFilenameImageSerializer(serializers.ModelSerializer):
    image = Base64WithFilenameImageField(required=False)

    class Meta:
        model = SampleBase64ImageModel
        fields = (
            'id',
            'image',
        )


class SampleBase64WithFilenameFileSerializer(serializers.ModelSerializer):
    file = Base64WithFilenameFileField(required=False)

    class Meta:
        model = SampleBase64FileModel
        fields = (
            'id',
            'file',
        )
