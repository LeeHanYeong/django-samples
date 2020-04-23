import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from members.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = None

    @database_sync_to_async
    def get_history(self, from_user_id, to_user_id):
        print('-- db.get_history --')
        return User.objects.get(id=from_user_id).get_history(to_user_id)

    @database_sync_to_async
    def update_history(self, content):
        print('-- db.save_history --')
        self.history.content += f'{content}\n'
        self.history.save()

    async def connect(self):
        print(f'- connect -')
        self.user_id = self.scope['url_route']['kwargs']['from_user_id']
        self.to_user_id = self.scope['url_route']['kwargs']['to_user_id']
        print('from_user:', self.user_id)
        print('to_user  :', self.to_user_id)
        self.history = await self.get_history(self.user_id, self.to_user_id)
        self.content = self.history.content

        # UserChatHistory의 id를 기준으로 Room의 이름을 정함
        self.room_name = f'{self.history.id}'
        self.room_group_name = f'chat_{self.room_name}'
        print(self.room_name)
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        print(f'- disconnect (code: {code}) -')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        print('- receive -')
        text_data_json = json.loads(text_data or '{}')
        message = text_data_json.get('message')
        await self.update_history(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def close(self, code=None):
        print(f'- close (code:{code}) -')
        await super().close(code)
