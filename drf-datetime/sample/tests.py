from django.test import TestCase
from model_bakery import baker
from .models import Post
from .serializers import PostSerializer


class DRFDateTimeFieldTest(TestCase):
    def test_timezone(self):
        post = baker.make(Post, timezone='Asia/Seoul')
        serializer1 = PostSerializer(post)
        data = serializer1.data
        print(data['dt'])

        serializer2 = PostSerializer(post)
