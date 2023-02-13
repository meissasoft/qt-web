import socket


class Client:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

    def send_message(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f'Response from server: {response}')
        client_socket.close()


if __name__ == '__main__':
    client = Client()
    client.send_message('take scan')
