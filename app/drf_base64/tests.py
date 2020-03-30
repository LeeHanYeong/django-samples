import base64
import filecmp
import os

from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SampleBase64ImageModel

PATH_IMAGE = finders.find(os.path.join('drf_base64', 'image', 'sample_jpg.jpg'))
PATH_BASE64_STR = finders.find(os.path.join('drf_base64', 'image', 'sample_jpg.txt'))
PATH_IMAGE_PNG = finders.find(os.path.join('drf_base64', 'image', 'sample_png.png'))
PATH_BASE64_STR_PNG = finders.find(os.path.join('drf_base64', 'image', 'sample_png.txt'))


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
    URL = '/drf_base64/image/'

    def test_create(self):
        base64_str = open(PATH_BASE64_STR, 'rt').read()
        response = self.client.post(self.URL, {'image': base64_str})
        self.assertIsNotNone(response.data['image'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 1)
        instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))


class Base64WithFilenameImageAPITest(APITestCase):
    URL = '/drf_base64/image-name/'

    def _create_instance(self):
        file = SimpleUploadedFile(os.path.basename(PATH_IMAGE), open(PATH_IMAGE, 'rb').read())
        return baker.make(SampleBase64ImageModel, image=file)

    def test_create(self):
        base64_str = open(PATH_BASE64_STR, 'rt').read()
        data = {
            'image': {
                'file_name': 'pby.jpg',
                'base64_data': base64_str,
            }
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertIsNotNone(response.data['image'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 1)
        instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))
        self.assertTrue('pby' in instance.image.name)

    def test_create_blank_null(self):
        data1 = {'image': None}
        data2 = {'image': ''}
        for data in (data1, data2):
            response = self.client.post(self.URL, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNone(response.data['image'])

            instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
            self.assertFalse(instance.image)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 2)

    def test_create_failed(self):
        pass

    def test_update(self):
        base64_str_png = open(PATH_BASE64_STR_PNG, 'rt').read()
        instance = self._create_instance()
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))

        # Retrieve/Update URL
        url = self.URL + f'{instance.pk}/'

        retrieve_response = self.client.get(url)
        retrieve_data = retrieve_response.data
        data = {
            **retrieve_data,
            'image': {
                'file_name': 'weepinmie.png',
                'base64_data': base64_str_png,
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(updated_instance.image.path, PATH_IMAGE_PNG))

    def test_update_blank_null(self):
        for value in (None, ''):
            instance = self._create_instance()
            self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))

            # Retrieve/Update URL
            url = self.URL + f'{instance.pk}/'

            retrieve_response = self.client.get(url)
            retrieve_data = retrieve_response.data

            data = {**retrieve_data, 'image': value}
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertIsNone(response.data['image'])
            updated_instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
            self.assertFalse(updated_instance.image)

    def test_update_ignore_url(self):
        """
        When an update is requested using the response data received by list or retrieve,
        Pass validation and verify that the field's value does not change
        """
        instance = self._create_instance()

        # Retrieve/Update URL
        url = self.URL + f'{instance.pk}/'

        retrieve_response = self.client.get(url)
        retrieve_data = retrieve_response.data
        retrieve_url = retrieve_data['image']

        update_response = self.client.patch(url, retrieve_data, format='json')
        update_data = update_response.data
        update_url = update_data['image']
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_url, update_url)
