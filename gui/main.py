import pygame
import pygame_menu


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        # Tạo đối tượng Menu
        self.menu = pygame_menu.Menu(
            'Main Menu', width, height, theme=pygame_menu.themes.THEME_BLUE)

        # Thêm các tùy chọn vào menu
        self.menu.add.button('Start the game', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def start_the_game(self):
        # Chuyển đến trò chơi
        game_loop()

    def show(self):
        # Hiển thị menu
        self.menu.mainloop(self.screen)

# Vòng lặp chính của trò chơi
def game_loop():
    # Làm gì đó ở đây
    pass
    # Khởi tạo pygame

pygame.init()
# Khởi tạo màn hình
screen = pygame.display.set_mode((640, 480))

# Tạo đối tượng MainMenu
main_menu = MainMenu(screen, 640, 480)

# Hiển thị menu
main_menu.show()
