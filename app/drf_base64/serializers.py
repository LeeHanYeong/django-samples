from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import SampleBase64ImageModel


class SampleBase64ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = SampleBase64ImageModel
        fields = (
            'id',
            'image',
        )
