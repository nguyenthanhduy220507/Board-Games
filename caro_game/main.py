import pygame
from caro_game.setting import WINDOW_HEIGHT, WINDOW_WIDTH
from pygame.image import load
from pygame.mouse import get_pressed as mouse_button
from caro_game.editor import Editor

class Caro:
    def __init__(self, connection, username=None):
        self.connection = connection
        self.username = username

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.editor = Editor()
        #cursor
        surf = load('./img/watermelon_cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0),surf)
        pygame.mouse.set_cursor(cursor)

    def mouse_event(self):
        if self.editor.playing and mouse_button()[0]:
                (x, y) = self.editor.get_current_cell()
                self.editor.left_mouse_click(x, y)
                print((x, y))
                self.connection.send(f'Game:::{x}:::{y}'.encode('utf-8'))
