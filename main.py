import pygame
from main_menu import MainMenu
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    MainMenu().run()