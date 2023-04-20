import socket
import sys
import threading

import pygame

from chat_gui import GUI
from caro_game.main import Caro

class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.gui = PlaySurface(self.sock)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8').split(':::')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.gui.game_gui_window.mouse_click(x, y)
                elif message[0] == 'Chat':
                    self.gui.chat_gui_window.add_message(str(message[1]))
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

        self.gui = PlaySurface(self.conn)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8').split(':::')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.gui.game_gui_window.mouse_click(x, y)
                elif message[0] == 'Chat':
                    self.gui.chat_gui_window.add_message(str(message[1]))
            except OSError:
                break

    def send(self, message):
        self.conn.sendall(message.encode('utf-8'))

class PlaySurface:
    def __init__(self, connection):
        self.connection = connection
        self.chat_gui_window = GUI(connection)
        self.game_gui_window = Caro(connection)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.game_gui_window.mouse_event(event)

            pygame.display.update()
            self.chat_gui_window.window.update()