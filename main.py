import socket
import threading
from caro_game.main import Caro
from chat_gui import Chat


class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.game_gui = Caro(self.sock)
        self.chat_gui = Chat(self.sock)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8').split('::')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.game_gui.clicked(x, y)
                elif message[0] == 'Chat':
                    self.chat_gui.add_message(message[1])
            except OSError:
                break


class Server:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()

        self.game_gui = Caro(self.conn)
        self.chat_gui = Chat(self.conn)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8').split(',')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.game_gui.clicked(x, y)
                elif message[0] == 'Chat':
                    self.chat_gui.add_message(message[1])
            except OSError:
                break

    def send(self, message):
        self.conn.sendall(message.encode('utf-8'))


class GUI:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

    def start_client(self):
        self.client = Client(self.host, self.port, self.username)
        threading.Thread(target=self.start_client_game).start()
        threading.Thread(target=self.start_client_chat).start()

    def start_client_game(self):
        self.client.game_gui.run()

    def start_client_chat(self):
        self.client.chat_gui.window.mainloop()

    def start_server(self):
        self.server = Server(self.host, self.port, self.username)
        threading.Thread(target=self.start_server_game).start()
        threading.Thread(target=self.start_server_chat).start()

    def start_server_game(self):
        self.server.game_gui.run()

    def start_server_chat(self):
        self.server.chat_gui.window.mainloop()


if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")

    if mode == 'server':
        username = input("Enter username: ")
        gui = GUI('', 55843, username)
        print(socket.gethostbyname(socket.gethostname()))
        gui.start_server()
    elif mode == 'client':
        host = input("Enter server IP address: ")
        port = int(input("Enter server port: "))
        username = input("Enter username: ")
        gui = GUI(host, port, username)
        gui.start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")
