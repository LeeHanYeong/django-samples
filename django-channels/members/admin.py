from django.contrib import admin

from members.models import UserChatHistory


@admin.register(UserChatHistory)
class UserChatHistoryAdmin(admin.ModelAdmin):
    pass
