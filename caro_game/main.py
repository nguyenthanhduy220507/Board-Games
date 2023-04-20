import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
from caro_game.board import Board


class Caro:
    def __init__(self, connection, username=None):
        self.connection = connection
        self.username = username
        self.window = pygame.display.set_mode((640, 640))

        self.cas = self.window
        self.board = Board()
        self.board.vehinh(self.cas)
        self.board.condition = 1

    def mouse_click(self, x, y):
        self.board.click_flag_box(self.cas, x, y)

    def mouse_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            self.mouse_click(x, y)
            self.connection.send(f'Game:::{x}:::{y}'.encode('utf-8'))

