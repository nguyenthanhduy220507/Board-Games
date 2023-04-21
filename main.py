import pygame
from main_menu import MainMenu
if __name__ == '__main__':
    pygame.init()
    try:
        MainMenu().run()
    except Exception:
        pass