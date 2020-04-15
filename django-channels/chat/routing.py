from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:from_user_id>/<int:to_user_id>/', consumers.ChatConsumer),
]
