from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    chat_users = models.ManyToManyField(
        'self', through='UserChatHistory', symmetrical=True, blank=True,
    )

    def __str__(self):
        return f'{self.id}'

    def get_history(self, other: User):
        other_id = other if isinstance(other, int) else other.id
        if self.chat_users.filter(id=other_id).exists():
            try:
                return self.user1_chat_history_set.get(user2=other)
            except UserChatHistory.DoesNotExist:
                try:
                    return self.user2_chat_history_set.get(user1=other)
                except UserChatHistory.DoesNotExist:
                    pass
        else:
            self.chat_users.add(other)
            return self.user1_chat_history_set.get(user2=other)


class UserChatHistory(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='user1_chat_history_set',
        blank=True, null=True)
    user2 = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='user2_chat_history_set',
        blank=True, null=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_user1_user2'),
        ]

    def __str__(self):
        return '[{id}] (User1: {user1}, User2: {user2})'.format(
            id=self.id,
            user1=self.user1.id,
            user2=self.user2.id,
        )
