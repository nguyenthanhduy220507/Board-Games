import pygame
import numpy as np
import sys
from GameSettings.DefaultSettings import *
from GameSettings import LightTheme
from GameSettings import Caro20x20

class BoardGUI():
    def __init__(self, screen, theme, row, col):
        super().__init__(row, col)
        self.screen = screen
        self.theme = theme
        self.size = Caro20x20
        self.number_score_to_win = self.size.number_square_to_win

    def drawBoardGames(self):
        self.screen.fill(self.theme.background_color)
        # Draw vertical lines
        x_index = self.square_size
        for col in range(self.board_col):
            pygame.draw.line(self.screen, self.theme.line_color, (x_index, 0), (x_index, board_height), self.size.line_width)
            x_index += self.square_size
        # Draw horizontal lines
        y_index = self.square_size
        for row in range(self.board_col):
            pygame.draw.line(self.screen, self.theme.line_color, (0, y_index), (board_width, y_index), self.size.line_width)
            y_index += self.square_size

width, height = 640, 640
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Trò chơi cờ caro')

def run():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

run()