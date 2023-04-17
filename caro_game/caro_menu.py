import pygame
import pygame_menu

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from caro_game.caro import Caro

class CaroMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Set theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title = False

        self.menu = pygame_menu.Menu(
            width=SCREEN_WIDTH, 
            height=SCREEN_HEIGHT, 
            title='',
            center_content=False,
            theme=theme,
        )

        self.menu.add.label(
            title='Caro Game',
            background_color='#333',
            background_inflate=(30, 0),
            float=True  # Widget does not add size to the menu
        ).translate(0, 5)
        
        self.surface = Caro(1,2).my_surface
        self.menu.add.surface(self.surface, align=pygame_menu.locals.ALIGN_LEFT).translate(10, 60)
        
        # Bottom scrollable text
        self.f = self.menu.add.frame_v(
            background_color='#333',
            border_color='#255',
            border_width=1,
            float=True,
            height=10000,
            max_height=600,
            width=400,
            align=pygame_menu.locals.ALIGN_RIGHT
        )
        self.f.relax(True)
        self.f.translate(0, 63)
        labels = self.menu.add.label('Chat Box', font_size=40, font_color='#fff', padding=5)
        self.f.pack(labels)

        def send_message_event(current_text):
            self.send_message(current_text)
            self.input_text.set_value('')

        self.input_text = self.menu.add.text_input(
            '',
            maxchar=40,
            copy_paste_enable=True,
            align=pygame_menu.locals.ALIGN_RIGHT,
            font_name=pygame_menu.font.FONT_FIRACODE,
            font_size=12,
            input_underline='_',
            onreturn=send_message_event
        ).translate(-20,10)
        

    def send_message(self, message):
        if (message == ''): return
        label = self.menu.add.label(f'  > {message}', font_size=12, font_color='#fff', padding=0)
        self.f.pack(label)

    def run(self):
        self.menu.mainloop(self.screen)