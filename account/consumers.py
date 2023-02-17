import asyncio
import json
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'machine_name' in text_data_json:
            bearer_token = text_data_json.get('token')
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


