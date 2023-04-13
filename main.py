import pygame
import pygame_menu
from chess_game.chess import Chess
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load image
        default_image = pygame_menu.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
        ).scale(0.2, 0.2)
        
        self.clock = pygame.time.Clock()
        # Set theme
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title = False

        self.modes = {
            1: {
                'image': default_image.copy(),
                'label': {
                    'color': theme.widget_font_color,
                    'size': theme.widget_font_size,
                    'text': 'The first one is very epic'
                }
            },
            2: {
                'image': default_image.copy().to_bw(),
                'label': {
                    'color': (0, 0, 0),
                    'size': 20,
                    'text': 'This other one is also epic, but fancy'
                }
            },
            3: {
                'image': default_image.copy().flip(False, True).pick_channels('r'),
                'label': {
                    'color': (255, 0, 0),
                    'size': 45,
                    'text': 'YOU D I E D'
                }
            }
        }

        self.menu = pygame_menu.Menu(
            width=SCREEN_WIDTH, 
            height=SCREEN_HEIGHT, 
            title='',
            center_content=False,
            theme=theme,
        )
        self.menu.add.label(
            'My App',
            background_color='#333',
            background_inflate=(30, 0),
            float=True  # Widget does not add size to the menu
        ).translate(0, 10)

        self.label = self.menu.add.label(
            'Lorem ipsum',
            float=True,
            font_name=pygame_menu.font.FONT_OPEN_SANS_ITALIC,
            font_size=25)
        self.label.rotate(90)
        self.label.translate(300, 160)

        self.user_name = self.menu.add.text_input('Name: ', default='John Doe', maxchar=10)
        self.selector_widget = self.menu.add.selector(
            title='Pick one option: ',
            items=[('The first', 1),
                   ('The second', 2),
                   ('The final mode', 3)],
            onchange=self.on_selector_change
        )
        self.image_widget = self.menu.add.image(
            image_path=self.modes[1]['image'],
            padding=(25, 0, 0, 0)  # top, right, bottom, left
        )

        self.item_description_widget = self.menu.add.label(title='')
        self.create_button = self.menu.add.button('Create', self.start_game)
        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT)
    

    def _update_from_selection(self, index: int) -> None:
        """
        Change widgets depending on index.
        :param index: Index
        """
        self.current = index
        self.image_widget.set_image(self.modes[index]['image'])
        self.item_description_widget.set_title(self.modes[index]['label']['text'])
        self.item_description_widget.update_font(
            {'color': self.modes[index]['label']['color'],
             'size': self.modes[index]['label']['size']}
        )

    def on_selector_change(self, selected, value):
        print('Selected data:', selected)
        self._update_from_selection(value)

    def start_game(self):
        # Tạo một Surface widget với một pygame.Surface
        print(f'{self.user_name.get_value()}, Do the job here!')
        chess = Chess(1, 2)
        surface_widget = pygame_menu.widgets.SurfaceWidget(surface=chess.my_surface)

        self.menu.add.generic_widget(surface_widget)
    
    def run(self):
        self.menu.mainloop(self.screen)


if __name__ == '__main__':
    MainMenu().run()
