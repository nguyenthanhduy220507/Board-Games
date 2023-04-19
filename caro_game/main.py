import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
from caro_game.board import Board


class Caro:
    def __init__(self, connection):
        self.connection = connection
        pygame.init()
        self.window = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Caro")
        self.clock = pygame.time.Clock()

        self.cas = self.window
        self.banco = Board()
        self.banco.vehinh(self.cas)
        self.banco.condition = 1

    def clicked(self, x, y):
        self.banco.click_flag_box(self.cas, x, y)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.clicked(x, y)
                    self.connection.send(f'Game::{x}::{y}'.encode('utf-8'))
            pygame.display.update()
            self.clock.tick(60)
