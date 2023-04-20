import functools
import queue
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
        self.message_queue = queue.Queue()

        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8').split(':::')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.gui.game_gui_window.mouse_click(x, y)
                elif message[0] == 'Chat':
                    self.message_queue.put(message[1])
            except OSError:
                break

    def update_chat_gui(self):
        try:
            message = self.message_queue.get_nowait()
            self.gui.chat_gui_window.add_message(str(message))
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)

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
        self.message_queue = queue.Queue()

        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)
        
    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8').split(':::')
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    self.gui.game_gui_window.mouse_click(x, y)
                elif message[0] == 'Chat':
                    self.message_queue.put(message[1])
            except OSError:
                break

    def update_chat_gui(self):
        try:
            message = self.message_queue.get_nowait()
            self.gui.chat_gui_window.add_message(str(message))
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)

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