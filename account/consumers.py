import json
import asyncio
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bearer_token = text_data_json.get('token')
        del text_data_json['token']
        headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:8000/api/user/user-connection/', data=text_data_json,
                                    headers=headers) as resp:
                response_text = await resp.text()
                # Do something with the response, like sending it back to the WebSocket client
                await self.send(text_data=response_text)


# import json
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
#
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'
#
#         # async_to_sync(self.channel_layer.group_add)(
#         #     self.room_group_name,
#         #     self.channel_name
#         # )
#
#         self.accept()
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps({
#             'type': 'chat',
#             'message': message
#         }))
