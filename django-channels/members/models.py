from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class ChatHistoryNotExist(Exception):
    def __str__(self):
        return 'ChatHistoryNotExist!'


class User(AbstractUser):
    chat_users = models.ManyToManyField('self', through='UserChatHistory', symmetrical=False, blank=True)

    def __str__(self):
        return f'{self.id}'

    def get_history(self, other_id):
        other = User.objects.get(id=other_id)
        try:
            history = UserChatHistory.objects.get(
                Q(from_user=self, to_user=other) |
                Q(from_user=other, to_user=self)
            )
        except UserChatHistory.DoesNotExist:
            history = self.chat_history_set_by_from_user.create(to_user=other)
        return history


class UserChatHistory(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='chat_history_set_by_from_user',
        blank=True, null=True)
    to_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='chat_history_set_by_to_user',
        blank=True, null=True)
    content = models.TextField('채팅 기록', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_users'),
        ]

    def __str__(self):
        return '[{id}] ChatHistory(From: {from_user}, To: {to_user})'.format(
            id=self.id,
            from_user=self.from_user.id,
            to_user=self.to_user.id,
        )
