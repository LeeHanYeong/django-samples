from django.test import TestCase
from model_bakery import baker

from members.models import User


class HistoryTest(TestCase):
    def test_m2m_history(self):
        user1, user2 = baker.make(User, _quantity=2)
        user1.chat_users.add(user2)
        self.assertTrue(user1.chat_users.filter(id=user2.id))
        self.assertTrue(user2.chat_users.filter(id=user1.id))
