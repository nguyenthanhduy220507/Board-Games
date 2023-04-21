import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional

from settings import WINDOW_SIZE, ABOUT, FPS, RETURN_MAIN_MENU_STR
from play_surface import Server, Client

class MainMenu:
    def __init__(self):
        self.clock: Optional['pygame.time.Clock'] = None
        self.main_menu: Optional['pygame_menu.Menu'] = None
        self.surface: Optional['pygame.Surface'] = None
        
    def main_background(self):
        self.surface.fill((128, 128, 128))

    def start_click(self):
        username = self.username_server_text.get_value()
        if not username: return
        Server('', 55843, username, self.surface)

    def join_click(self):
        ip_address = self.ip_address_text.get_value()
        if not ip_address: return
        username = self.username_client_text.get_value()
        if not username: return
        Client(ip_address, 55843, username)

    def run(self):
        self.surface = create_example_window('Example - Game Selector', WINDOW_SIZE)
        self.clock = pygame.time.Clock()

        self.play_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.7,
            title='Play Menu',
            width=WINDOW_SIZE[0] * 0.75
        )

        self.start_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.5,
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Start Server',
            width=WINDOW_SIZE[0] * 0.7
        )
        self.username_server_text = self.start_server_menu.add.text_input(title='Username: ')
        self.start_server_menu.add.button('Start', self.start_click)
        self.start_server_menu.add.button(RETURN_MAIN_MENU_STR, pygame_menu.events.RESET)
        

        self.join_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.5,
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Join Server',
            width=WINDOW_SIZE[0] * 0.7
        )
        self.ip_address_text = self.join_server_menu.add.text_input(title='IP address: ')
        self.username_client_text = self.join_server_menu.add.text_input(title='Username: ')
        self.join_server_menu.add.button('Join', self.join_click)
        self.join_server_menu.add.button(RETURN_MAIN_MENU_STR, pygame_menu.events.RESET)

        self.play_menu.add.button('Start server', self.start_server_menu)
        self.play_menu.add.button('Join server', self.join_server_menu)
        self.play_menu.add.button(RETURN_MAIN_MENU_STR, pygame_menu.events.BACK)

        about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        about_theme.widget_margin = (0, 0)

        self.about_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.6,
            theme=about_theme,
            title='About',
            width=WINDOW_SIZE[0] * 0.6
        )

        for m in ABOUT:
            self.about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
        self.about_menu.add.vertical_margin(30)
        self.about_menu.add.button(RETURN_MAIN_MENU_STR, pygame_menu.events.BACK)

        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

        self.main_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.6,
            theme=main_theme,
            title='Main Menu',
            width=WINDOW_SIZE[0] * 0.6
        )

        self.main_menu.add.button(title='Play', action=self.play_menu)
        self.main_menu.add.button('About', self.about_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        self.main_background()
        
        while True:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.main_menu.is_enabled():
                self.main_menu.mainloop(self.surface, self.main_background, fps_limit=FPS)

            pygame.display.update()