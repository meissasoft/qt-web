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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = None
        self.host = '127.0.0.1'
        self.port = 4444
        self.ws = 'ws://127.0.0.1:8000/ws/socket-server/'

    def login(self, username, password):
        login_data = {
            'email': username,
            'password': password,
        }
        login_response = self._send_request(login_data)
        self.token = login_response.get('token').get('access')
        if not self.token:
            raise Exception('Login failed')

    def _send_request(self, payload):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        response = requests.request("POST", 'http://127.0.0.1:8000/api/user/login/',
                                    headers=headers,
                                    data=payload)
        return response.json()

    def send_message_to_itgnir(self, message):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(message.encode())
        response = self.client_socket.recv(1024).decode()
        return response

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
            response = await websocket.recv()
            data = json.loads(response)
            if data['is_scan'] == 'yes':
                scan_data = self.send_message_to_itgnir('take scan')

    async def amain(self):
        await self.send_system_data_request()

    def main(self):
        self.login('software@gmail.com', '$@lm@n123')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.amain())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
        # threading.Thread(target=self.receive_loop).start()
        # threading.Thread(target=self.send_loop).start()


if __name__ == "__main__":
    service = DjangoWebsocketService('ws://127.0.0.1:8000')
    service.main()
