import pygame
import pygame_menu

from chess_game.chess_menu import ChessMenu

class ServerCreate:
    def __init__(self, game_choice):
        self.screen = pygame.display.set_mode((640, 400))

        self.game = None

        if game_choice == 'chess':
            self.game = ChessMenu()


        # Set theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title = False

        self.menu = pygame_menu.Menu(
            width=640,
            height=400,
            title='',
            theme=theme,
        )

        self.menu.add.label(
            title='Server Settings',
            background_color='#333',
            background_inflate=(30, 0),
        ).translate(0, -10)

        self.host_server = self.menu.add.button(
            title='Host Server',
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            action=None
        )

        self.client = self.menu.add.text_input(
            title='Enter IP Server: ',
            align=pygame_menu.locals.ALIGN_LEFT,
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            default='http://127.0.0.1:5500/',
            maxchar=30,
            input_underline='_'
        )

        self.start = self.menu.add.button(
            title='Create',
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            action=lambda: self.start_game(self.game)
        )

        self.quit_button = self.menu.add.button(
            title='Quit',
            font_name=pygame_menu.font.FONT_OPEN_SANS,
            action=pygame_menu.events.EXIT
        )
    

    def _update_from_selection(self, index: int):
        self.current = index
        self.create_button.update_callback(self.modes[index]['action'])

    def on_selector_change(self, selected, value):
        print('Selected data:', selected)
        self._update_from_selection(value)

    def start_game(self, game_menu):
        game_menu.run()
    
    def run(self):
        self.menu.mainloop(self.screen)