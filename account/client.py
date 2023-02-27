import socket


class Client:
    def __init__(self, host='127.0.0.1', port=4444):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(message.encode())
        response = self.client_socket.recv(1024).decode()
        return response
        # print(f'Response from server: {response}')
        # client_socket.close()


# if __name__ == '__main__':
#     client = Client()
#     client.send_message('take scan')
