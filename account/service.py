import asyncio
import json
import threading
import time
import uuid
import socket
import requests
import websockets


class DjangoWebsocketService:
    def __init__(self, django_server_url):
        self.django_server_url = django_server_url
        self.token = None
        self.ws = None

    def login(self, username, password):
        login_data = {
            'email': 'software@gmail.com',
            'password': '$@lm@n123',
        }
        login_response = self._send_request('/api/user/login/', login_data)
        self.token = login_response.get('token').get('access')
        if not self.token:
            raise Exception('Login failed')

    def connect(self):
        if not self.token:
            raise Exception('Not logged in')
        websocket_url = self.django_server_url.replace('http', 'ws') + '/ws/' + 'socket-server/'

        self.ws = websockets.connect(websocket_url)
        # self.ws.run_forever()

    def _send_request(self, path, payload):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        response = requests.request("POST", 'http://127.0.0.1:8000/api/user/login/',
                                    headers=headers,
                                    data=payload)
        return response.json()

    def receive_loop(self):
        while True:
            message = self.ws.recv()
            message_data = json.loads(message)
            # Handle received message data here as necessary

    async def send_system_data_request(self):
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8 * 6, 8)][::-1])

        machine_name = socket.gethostname()
        request_data = {
            'token': self.token,
            'mac_address': mac_address,
            'machine_name': machine_name
        }
        async with websockets.connect(self.django_server_url + '/ws/socket-server/') as websocket:
            await websocket.send(json.dumps(request_data))
            # print(f'Sent message: {request_data}')
        # self.ws.send(json.dumps(request_data))

    async def amain(self):
        await self.send_system_data_request()

    def main(self):
        self.login('username', 'password')
        self.connect()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.amain())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
        threading.Thread(target=self.receive_loop).start()
        # threading.Thread(target=self.send_loop).start()


if __name__ == "__main__":
    service = DjangoWebsocketService('ws://127.0.0.1:8000')
    service.main()
