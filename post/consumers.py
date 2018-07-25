from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class PostConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'post_ws'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'new.post',
                'message': message
            }
        )

    def new_post(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
