from django.test import TestCase
from model_bakery import baker

from members.models import User


class HistoryTest(TestCase):
    def test_m2m_history(self):
        user1, user2 = baker.make(User, _quantity=2)
        history = user1.get_history(user2.id)
        self.assertEqual(history.from_user, user1)
        self.assertEqual(history.to_user, user2)
