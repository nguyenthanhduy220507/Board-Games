import queue
import socket
import sys
import threading

import pygame
import pygame_menu

from chat_gui import GUI
from caro_game.main import Caro
from settings import WINDOW_SIZE

class Client:
    def __init__(self, host, port, username, main_menu):
        self.host = host
        self.port = port
        self.username = username
        self.main_menu = main_menu

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.gui = PlaySurface(self.sock, username)
        self.message_queue = queue.Queue()

        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)
        self.gui.run(main_menu)

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
            except Exception:
                print(str(Exception))
                self.sock.close()
                self.gui.close(self.main_menu)
                break

    def update_chat_gui(self):
        try:
            message = self.message_queue.get_nowait()
            self.gui.chat_gui_window.add_message(str(message))
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)

class Server:
    def __init__(self, host, port, username, surface, main_menu):
        self.host = host
        self.port = port
        self.username = username
        self.main_menu = main_menu

        self.connected = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        loading = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.5,
            title='Waiting for client',
            width=WINDOW_SIZE[0] * 0.7
        )
        loading.add.label(title=f'IP Address:{socket.gethostbyname(socket.gethostname())}')
        threading.Thread(target=self.accepted_connect).start()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.sock.close()
                    pygame.quit()
                    sys.exit()
            if self.connected:
                break
            if loading.is_enabled():
                loading.update(events)
                loading.draw(surface)
            pygame.display.update()
        loading.disable()
        self.gui = PlaySurface(self.conn, username)
        self.message_queue = queue.Queue()
        threading.Thread(target=self.receive, daemon=True).start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)
        self.gui.run(main_menu)

    def accepted_connect(self):
        try:
            self.conn, self.addr = self.sock.accept()
        except Exception: pass
        self.connected = True
        
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
            except Exception:
                print(str(Exception))
                self.conn.close()
                self.gui.close(self.main_menu)
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
    def __init__(self, connection, username):
        self.connection = connection
        self.chat_gui_window = GUI(connection, username)
        self.game_gui_window = Caro(connection, username)

    def run(self, main_menu):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.chat_gui_window.window.destroy()
                    main_menu()
                    self.connection.close()
                    return
                self.game_gui_window.mouse_event(event)

            pygame.display.update()
            self.chat_gui_window.window.update()
    
    def close(self, main_menu):
        self.chat_gui_window.window.destroy()
        main_menu()