import pygame
from caro_game.settings import WINDOW_HEIGHT, WINDOW_WIDTH, CURSOR_IMAGE
from pygame.image import load
from pygame.mouse import get_pressed as mouse_button
from caro_game.editor import Editor

class Caro:
    def __init__(self, connection, host, port, username=None, competitor_name=None):
        self.connection = connection
        self.host = host
        self.port = port
        self.username = username

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.editor = Editor(username, competitor_name)
        #cursor
        surf = load(CURSOR_IMAGE).convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0),surf)
        pygame.mouse.set_cursor(cursor)
        self.clicked = False

    def mouse_event(self):
        if self.editor.playing and mouse_button()[0] and not self.clicked:
            (x, y) = self.editor.get_current_cell()
            if self.editor.left_mouse_click(x, y):
                self.connection.sendto(f'Game:::{x}:::{y}:::'.encode('utf-8'), (self.host, self.port))
                self.clicked = True

    def event_loop(self, event):
        self.editor.pan_input(event)
        #bấm enter để chơi lại
        if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_RETURN:
            self.clicked = False
            self.editor.play_again()
            self.connection.sendto(b'Play again', (self.host, self.port))
