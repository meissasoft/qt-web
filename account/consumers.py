import jwt
import asyncio
import json
import aiohttp
from rest_framework_simplejwt.tokens import AccessToken
from channels.generic.websocket import AsyncWebsocketConsumer

connections = {}


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    # async def send(self, text_data=None, bytes_data=None, close=False):
    #     await self.send(json.dumps(text_data))

    async def disconnect(self, close_code):
        pass

    async def get_user_id_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return user_id
        except Exception as e:
            # Handle invalid token
            raise Exception('Error: {e}')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'machine_name' in text_data_json:
            bearer_token = text_data_json.get('token')
            user_id = await self.get_user_id_from_token(bearer_token)
            global connections
            connections[user_id] = self
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:8000/api/user/user-connection/', data=text_data_json,
                                        headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'is_scan': 'no'}
                    # await self.send(text_data=json.dumps(response))
                    # send message to server
                    await self.send(json.dumps(response))

        elif text_data_json['is_scan_data'] == 'yes':
            user_id = text_data_json['user_id']
            # global connections
            # await connections[user_id].receive(json.dumps(text_data))

        elif 'wavelength' in text_data_json:
            bearer_token = text_data_json.get('token')
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:8000/api/user/scan-data/', data=text_data_json,
                                        headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'is_scan': 'yes'}
                    # await self.send(text_data=json.dumps(response))
                    # send message to server
                    await self.send(json.dumps(response))

        elif 'is_connection_alive' in text_data_json:
            bearer_token = text_data_json.get('token')
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.put('http://127.0.0.1:8000/api/user/user-connection/', data=text_data_json,
                                       headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'is_scan': 'yes'}
                    # await self.send(text_data=json.dumps(response))
                    # send message to server
                    await self.send(json.dumps(response))
        elif 'is_scan' in text_data_json:
            print("")




# import asyncio
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         pass
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get('type')
#
#         if message_type == 'message':
#             message_text = data.get('text')
#             # Do something with the message text, e.g. send a response
#             await self.send(json.dumps({'type': 'response', 'text': f'Received message: {message_text}'}))


# async def main():
#     # Example usage
#     client = ChatConsumer.as_asgi()
#     await client.connect()
#     await client.send(json.dumps({'type': 'message', 'text': 'Hello, server!'}))
#
#     while True:
#         await asyncio.sleep(1)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

