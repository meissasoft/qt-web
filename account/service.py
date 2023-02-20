import asyncio
import json
import threading
import time
import uuid
import socket
import requests
from websockets import connect


class DjangoWebsocketService:
    def __init__(self, django_server_url):
        self.django_server_url = django_server_url
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = None
        self.host = '127.0.0.1'
        self.port = 4444
        self.ws = 'ws://127.0.0.1:8000/ws/socket-server/'
        self.websocket = None

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

    async def connect_to_server(self):
        self.websocket = await connect(self.ws)

    async def send_data(self, data):
        if self.websocket:
            await self.websocket.send(json.dumps(data))

    async def receive_data(self):
        if self.websocket:
            print("waiting for receive")
            message = await self.websocket.recv()
            print("received", message)
            message_data = json.loads(message)
            # Handle received message data here as necessary
            if 'is_scan_data' in message_data.keys():
                await self.take_scan_loop(message)
            return message_data

    def send_message_to_itgnir(self, message):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(message.encode())
        response = self.client_socket.recv(1024).decode()
        return response

    async def send_system_data_request(self):
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8 * 6, 8)][::-1])

        machine_name = socket.gethostname()
        request_data = {
            'token': self.token,
            'mac_address': mac_address,
            'machine_name': machine_name
        }
        await self.send_data(request_data)
        response = await self.receive_data()
        print(response)

    async def take_scan_loop(self, data):
        # request_data = {'is_scan': 'yes'}
        print("receive")
        if data['is_scan_data'] == 'yes':
            scan_data = self.send_message_to_itgnir('take scan')
            scan_data = eval(scan_data)
            scan_data['token'] = self.token
            await self.send_data(scan_data)

    async def update_user_connection_status_loop(self):
        # send a "yes" message every minute to indicate that the connection is still alive
        request_data = {"is_connection_alive": "yes", "token": self.token}
        await self.send_data(request_data)
        await asyncio.sleep(60)

    def thread1(self):
        while True:
            self.take_scan_loop()

    def thread2(self):
        while True:
            self.update_user_connection_status_loop()

    async def amain(self):
        await self.connect_to_server()
        await self.send_system_data_request()
        # await self.update_user_connection_status_loop()
        await self.update_user_connection_status_loop()
        # thread1 = threading.Thread(target=self.thread1)
        # thread1.start()
        # thread2 = threading.Thread(target=self.thread2)
        # thread2.start()
        # websocket = websockets.connect(self.django_server_url + '/ws/socket-server/')
        # async with connect(self.ws) as websocket:
        #     await self.send_system_data_request(websocket)
        #     request_data = {'is_scan': 'yes'}
        #     thread1 = threading.Thread(target=self.thread1, args=(request_data, websocket))
        #     thread1.start()
        #     thread2 = threading.Thread(target=self.thread2, args=(websocket,))
        #     thread2.start()

    def main(self):
        self.login('softech@gmail.com', '$0ftw@re123')
        # self.login('computer@gmail.com', 'C0mputer123')
        # self.login('laptop@gmail.com', 'C0mputer123')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.amain())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()


if __name__ == "__main__":
    service = DjangoWebsocketService('ws://127.0.0.1:8000')
    service.main()
