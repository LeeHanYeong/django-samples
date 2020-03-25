import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data or '{}')
        message = text_data_json.get('message')

        self.send(text_data=json.dumps({
            'message': message,
        }))
