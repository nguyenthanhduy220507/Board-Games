import pygame
import pygame_menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))

        self.menu = pygame_menu.Menu(
            title='Welcome to board game',
            width=1080,
            height=720,
            theme=pygame_menu.themes.THEME_DEFAULT
        )

    def run(self):
        self.menu.mainloop(self.screen)


if __name__ == '__main__':
    menu = Game()
    menu.run()