# setup
import pygame


TILE_SIZE = 40
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640

LINE_COLOR = "black"

CURSOR_IMAGE = './img/watermelon_cursor.png'

EDITOR_DATA = [
    {'id': 'x', 'image': './img/mark_x_1.png'},
    {'id': 'o', 'image': './img/mark_o_1.png'}
]


# pygame.mixer.pre_init(frequency=44100, size = -16, channels= 2, buffer= 512)
pygame.mixer.init()
#chèn âm thanh
TICK_SOUND_X = pygame.mixer.Sound('./sound/tick_sound_X.wav')
TICK_SOUND_O = pygame.mixer.Sound('./sound/tick_sound_O.wav')
DRAW_WIN = pygame.mixer.Sound('./sound/draw_win3.wav')
SOUND_TRACK = pygame.mixer.Sound('./sound/sound_track_action .wav')

# Tạo một kênh âm thanh mới để phát các âm thanh X và O
GAME_SOUNDS = pygame.mixer.Channel(1)
# SOUND_TRACK_SOUNDS = pygame.mixer.Channel(0)
