import json
import time
import uuid
import socket
import asyncio
import requests
import telnetlib
import threading
import subprocess
import logging as log
from websockets import connect

log.basicConfig(
    filename=r'C:\Service_File\itgnir_log_file.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=log.DEBUG
)


class DjangoWebsocketService:
    def __init__(self):
        self.run_itgnir()
        self.tn = telnetlib.Telnet("localhost", 44444)
        self.scan = 'scan'
        self.continue_scan = 'continue'
        self.token = None
        self.ws = 'ws://131.239.80.179/api/ws/socket-server/'
        self.websocket = None

    def check_itgnir_network(self):
        output = subprocess.check_output('tasklist', shell=True, text=True)
        if "itgnir.exe" in output:
            return True

    def start_itgnir_network(self):
        path = r'C:\Service_File\itgnir.lnk'
        try:
            subprocess.run(f'{path} network', shell=True, check=True)
            log.info("ITGNIR has been started")
        except FileNotFoundError:
            log.info(f"{path} does not exist")
        except subprocess.CalledProcessError:
            log.info("Failed to start ITGNIR network")

    def run_itgnir(self):
        if self.check_itgnir_network():
            log.info("ITGNIR is already running")
        else:
            subprocess_thread = threading.Thread(target=self.start_itgnir_network)
            subprocess_thread.start()
            time.sleep(10)

    def login(self, username, password):
        try:
            login_data = {
                'email': username,
                'password': password,
            }
            login_response = self._send_request(login_data)
            self.token = login_response.get('token').get('access')
            if not self.token:
                raise Exception('Login failed')
        except:
            print(f'Error: User with email {username} and password {password} does not exits')

    def _send_request(self, payload):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        response = requests.request("POST", 'http://131.239.80.179/api/user/login/',
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
            log.info("waiting for receive")
            message = await self.websocket.recv()
            log.info(f"received {message}")
            message_data = json.loads(message)
            if 'is_scan_data' in message_data.keys():
                scan_id = message_data['scan_id']
                response = await self.take_scan_loop(message_data)
                response['scan_id'] = scan_id
                await self.send_data(response)
            return message_data

    # def send_commands_to_itgnir(self):
    #     self.tn = telnetlib.Telnet("localhost", 44444)
    #     self.scan = 'scan'
    #     self.continue_scan = 'continue'
    #     self.tn.write(self.scan.encode('ascii') + b'\n')
    #     self.tn.read_until(b'Scanning..')
    #     self.tn.write(self.continue_scan.encode('ascii') + b'\n')
    #     self.tn.read_until(b'SAMPLE')
    #     self.tn.write(self.continue_scan.encode('ascii') + b'\n')
    #     data = self.tn.read_until(b'Dump').decode('utf-8')
    #     log.info("data from itgnir", data)
    #     return data

    # Function to send a command and read the response

    def send_command_and_read_until(self, command, expected_response):
        self.tn.write(command.encode('ascii') + b'\n')
        response = self.tn.read_until(expected_response.encode('ascii'))
        return response.decode('utf-8')

    def send_commands_to_itgnir(self):
        # Send the scan command and read until "Scanning.."
        response = self.send_command_and_read_until(self.scan, 'Scanning..')
        time.sleep(2)
        # If the response does not contain "Scanning..", resend the scan command
        if 'Scanning..' not in response:
            self.send_command_and_read_until(self.scan, 'Scanning..')
        # Send the continue_scan command and read until "SAMPLE"
        response = self.send_command_and_read_until(self.continue_scan, 'SAMPLE')
        time.sleep(2)
        if 'SAMPLE' not in response:
            self.send_command_and_read_until(self.continue_scan, 'SAMPLE')
        # Send the continue_scan command again and read until "Dump"
        response = self.send_command_and_read_until(self.continue_scan, 'Dump')
        time.sleep(2)
        if 'Dump' not in response:
            response = self.send_command_and_read_until(self.continue_scan, 'Dump')

        log.info("data from itgnir: %s", response)
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
        log.info("local machine specifications", response)

    async def take_scan_loop(self, data):
        log.info("response")
        if data['is_scan_data'] == 'yes':
            response = self.send_commands_to_itgnir()
            return {'energy_wavelength_data': response, 'token': self.token}

    async def update_user_connection_status_loop(self):
        while True:
            # send a "yes" message every minute to indicate that the connection is still alive
            request_data = {"is_connection_alive": "yes", "token": self.token}
            await self.send_data(request_data)
            response = await self.receive_data()
            response = await self.receive_data()
            await asyncio.sleep(60)

    def thread1(self, data):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [loop.create_task(self.take_scan_loop(data))]
        loop.run_until_complete(asyncio.gather(*tasks))

    def thread2(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [loop.create_task(self.update_user_connection_status_loop())]
            loop.run_until_complete(asyncio.gather(*tasks))

    async def amain(self):
        await self.connect_to_server()
        await self.send_system_data_request()
        await self.update_user_connection_status_loop()

    def service_main(self):
        self.login('kellen2@gmail.com', '123456')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.run(self.amain())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()


if __name__ == '__main__':
    service_instance = DjangoWebsocketService()
    service_instance.service_main()