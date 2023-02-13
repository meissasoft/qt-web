import socket


class Server:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        print(f'Server listening on {self.host}:{self.port}')
        while True:
            conn, addr = server_socket.accept()
            message = conn.recv(1024).decode()
            if message == 'take scan':
                conn.sendall('ok'.encode())
            conn.close()


if __name__ == '__main__':
    server = Server()
    server.start()


