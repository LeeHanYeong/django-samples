import base64
import filecmp
import os

from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SampleBase64ImageModel

PATH_IMAGE = os.path.join(settings.STATIC_DIR, 'drf_base64', 'pby.jpg')
PATH_BASE64_STR = os.path.join(settings.STATIC_DIR, 'drf_base64', 'pby.txt')


class Base64ImageConvertTest(TestCase):
    def test_encode(self):
        content = open(PATH_IMAGE, 'rb').read()
        encoded_str = base64.b64encode(content).decode('utf-8')

        self.assertEqual(
            encoded_str, open(PATH_BASE64_STR, 'rt').read()
        )

    def test_decode(self):
        content = open(PATH_BASE64_STR, 'rb').read()
        decoded_str = base64.decodebytes(content)

        self.assertEqual(
            decoded_str, open(PATH_IMAGE, 'rb').read()
        )


class Base64ImageAPITest(APITestCase):
    URL = '/drf_base64/'

    def test_create(self):
        base64_str = open(PATH_BASE64_STR, 'rt').read()
        response = self.client.post(self.URL, {'image': base64_str})
        self.assertIsNotNone(response.data['image'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 1)
        instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))
