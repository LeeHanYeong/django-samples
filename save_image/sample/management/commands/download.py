import mimetypes
import os
# https://github.com/ahupp/python-magic
import magic

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from sample.models import SampleImageModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://img-cf.kurly.com/shop/data/goods/1583819891213y0.jpg'
        # URL(Path)로부터 파일이름을 알아내기
        basename = os.path.basename(url)
        print(basename)

        # URL에 GET요청, 결과 이진데이터를 받아옴
        response = requests.get(url)
        binary_data = response.content

        # 이진데이터로부터 해당 파일이 어떤 MIME-Type인지 알아내기
        mime_type = magic.from_buffer(binary_data, mime=True)
        print(mime_type)

        # MIME-Type에서부터 확장자를 가져오기
        ext = mimetypes.guess_extension(mime_type)
        print(ext)

        # Django의 SimpleUploadedFile을 사용해서 이미지필드를 포함한 모델 인스턴스 생성
        file = SimpleUploadedFile(basename, binary_data)
        instance = SampleImageModel.objects.create(image=file)
