import pygame
import pygame_menu

from chess_game.chess_menu import ChessMenu
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))

        # Set theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title = False

        self.modes = {
            1: {
                'action': lambda: self.start_game('caro'),
            },
            2: {
                'action': lambda: self.start_game('chess')
            },
        }

        self.menu = pygame_menu.Menu(
            width=SCREEN_WIDTH // 1.5, 
            height=SCREEN_HEIGHT // 1.5, 
            title='',
            center_content=False,
            theme=theme,
        )
        self.menu.add.label(
            title='Board Games',
            background_color='#333',
            background_inflate=(30, 0),
            float=True  # Widget does not add size to the menu
        ).translate(0, 10)

        self.user_name = self.menu.add.text_input(
            title='Name: ',
            align=pygame_menu.locals.ALIGN_LEFT,
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            default='John',
            maxchar=10,
            input_underline='_'
        ).translate(10, 140)
        
        self.selector_widget = self.menu.add.selector(
            title='Select game: ',
            items=[('Caro', 1),
                   ('Chess', 2)],
            align=pygame_menu.locals.ALIGN_LEFT,
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            onchange=self.on_selector_change
        ).translate(10, 150)

        self.create_button = self.menu.add.button(
            title='Start',
            align=pygame_menu.locals.ALIGN_LEFT,
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            action=lambda: self.start_game('caro')
        ).translate(10, 160)

        self.quit_button = self.menu.add.button(
            title='Quit',
            align=pygame_menu.locals.ALIGN_LEFT,
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            action=pygame_menu.events.EXIT
        ).translate(10, 170)
    

    def _update_from_selection(self, index: int):
        self.current = index

    def on_selector_change(self, selected, value):
        print('Selected data:', selected)
        self.create_button.update_callback(self.modes[value]['action'])

    def start_game(self, game_choice):
        pass
    
    def run(self):
        self.menu.mainloop(self.screen)


if __name__ == '__main__':
    MainMenu().run()
