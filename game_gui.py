import socket
import tkinter as tk
from threading import Thread
from caro_game.main import Caro

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.gui = Caro(self.sock)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8').split(',')
                x = int(message[0])
                y = int(message[1])
                self.gui.clicked(x, y)
            except OSError:
                break

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()

        self.gui = Caro(self.conn)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8').split(',')
                x = int(message[0])
                y = int(message[1])
                self.gui.clicked(x, y)
            except OSError:
                break

    def send(self, message):
        self.conn.sendall(message.encode('utf-8'))


def start_client():
    host = input("Enter server IP address: ")
    port = int(input("Enter server port: "))
    client = Client(host, port)
    client.gui.window.mainloop()

def start_server():
    host = ''
    port = 55843
    server = Server(host, port)
    server.gui.window.mainloop()

if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")
    if mode == 'server':
        print(socket.gethostbyname(socket.gethostname()))
        start_server()
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")