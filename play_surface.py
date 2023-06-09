import queue
import socket
import sys
import threading

import pygame
import pygame_menu

from chat_gui import GUI
from caro_game.main import Caro
from settings import WINDOW_SIZE

clickQueue = queue.Queue()


class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.competitor_name = 'Player 1'

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(f'Connected:::{self.username}'.encode('utf-8'), (self.host, self.port))
        self.gui = PlaySurface(self.sock, self.host, self.port, username, self.competitor_name, False)
        self.gui.game_gui_window.clicked = True
        self.message_queue = queue.Queue()
        self.close_queue = queue.Queue()

        threading.Thread(target=self.receive, daemon=True).start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)
        self.gui.chat_gui_window.window.after(100, self.close_chat_gui)
        self.gui.run()

    def receive(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                if data == b'Play again':
                    self.gui.game_gui_window.editor.play_again()
                    self.gui.game_gui_window.clicked = True
                    continue
                message = data.decode('utf-8').split(':::')
                print(message)
                if message[0] == 'Connected':
                    self.competitor_name = str(message[1])
                    self.gui.game_gui_window.competitor_name = str(message[1])
                    self.gui.game_gui_window.editor.competitor_name = str(message[1])
                elif message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    clickQueue.put(f'Clicked:::{x}:::{y}')
                elif message[0] == 'Chat':
                    self.message_queue.put(message[1])
            except OSError as e:
                print(str(e))
                self.sock.close()
                self.close_queue.put('Close connection')
                break

    def close_chat_gui(self):
        try:
            self.close_queue.get_nowait()
            self.gui.close()
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.close_chat_gui)

    def update_chat_gui(self):
        try:
            message = self.message_queue.get_nowait()
            self.gui.chat_gui_window.add_message(str(message))
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)


class Server:
    def __init__(self, host, port, username, surface):
        self.host = host
        self.port = port
        self.username = username
        self.competitor_name = 'Player 2'

        self.connected = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        loading = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.5,
            title='Waiting for client',
            width=WINDOW_SIZE[0] * 0.7
        )
        loading.add.label(
            title=f'IP Address:{socket.gethostbyname(socket.gethostname())}')
        threading.Thread(target=self.accepted_connect).start()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.connected:
                break
            if loading.is_enabled():
                loading.update(events)
                loading.draw(surface)
            pygame.display.update()
        loading.disable()
        self.gui = PlaySurface(self.sock, self.addr[0], self.addr[1], username, self.competitor_name, True)
        self.message_queue = queue.Queue()
        self.close_queue = queue.Queue()
        threading.Thread(target=self.receive, daemon=True).start()
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)
        self.gui.chat_gui_window.window.after(100, self.close_chat_gui)
        self.gui.run()

    def accepted_connect(self):
        while True:
            try:
                data, self.addr = self.sock.recvfrom(1024)
                message = data.decode('utf-8').split(':::')
                if message[0] == 'Connected':
                    self.connected = True
                    self.competitor_name = str(message[1])
                    self.sock.sendto(f'Connected:::{self.username}'.encode('utf-8'), self.addr)
                    break
                else:
                    self.connected = False
            except Exception:
                break

    def receive(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                if data == b'Play again':
                    self.gui.game_gui_window.editor.play_again()
                    self.gui.game_gui_window.clicked = False

                    continue
                message = data.decode('utf-8').split(':::')
                print(message)
                if message[0] == 'Game':
                    x = int(message[1])
                    y = int(message[2])
                    clickQueue.put(f'Clicked:::{x}:::{y}')
                elif message[0] == 'Chat':
                    self.message_queue.put(message[1])
            except OSError as e:
                print(str(e))
                self.sock.close()
                self.close_queue.put('Close connection')
                break

    def close_chat_gui(self):
        try:
            self.close_queue.get_nowait()
            self.gui.close()
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.close_chat_gui)

    def update_chat_gui(self):
        try:
            message = self.message_queue.get_nowait()
            self.gui.chat_gui_window.add_message(str(message))
        except queue.Empty:
            pass
        self.gui.chat_gui_window.window.after(100, self.update_chat_gui)


class PlaySurface:
    def __init__(self, connection, host, port, username, competitor_name=None, is_host=True):
        self.connection = connection
        self.chat_gui_window = GUI(connection, host, port, username)
        self.game_gui_window = Caro(connection, host, port, username, competitor_name, is_host)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.connection.close()
                    pygame.quit()
                    sys.exit()
                self.game_gui_window.event_loop(event)
                self.game_gui_window.mouse_event()

            if not clickQueue.empty():
                message = str(clickQueue.get()).split(":::")
                if self.game_gui_window.editor.left_mouse_click(int(message[1]), int(message[2])):
                    self.game_gui_window.clicked = False
            
            self.game_gui_window.clock.tick(60)
            
            self.game_gui_window.editor.run()
            pygame.display.update()
            self.chat_gui_window.window.update()

    def close(self):
        self.connection.close()
        pygame.quit()
        sys.exit()
