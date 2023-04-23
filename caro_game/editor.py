import pygame
from caro_game.setting import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE, EDITOR_DATA, LINE_COLOR
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_button
from pygame.mouse import get_pos as mouse_pos


pygame.mixer.pre_init(frequency=44100, size = -16, channels= 2, buffer= 512)
pygame.mixer.init()
#chèn âm thanh
tick_sound_x = pygame.mixer.Sound('sound/tick_sound_X.wav')
tick_sound_o = pygame.mixer.Sound('sound/tick_sound_O.wav')
draw_win = pygame.mixer.Sound('sound/draw_win3.wav')
sound_track = pygame.mixer.Sound('sound/sound_track2.wav')
# Tạo một kênh âm thanh mới để phát các âm thanh X và O
game_sounds = pygame.mixer.Channel(1)

class Editor():
    def __init__(self, username):
        self.username = username

        self.display_surface = pygame.display.get_surface()
        self.origin = vector()
        self.pain_active = False
        self.pain_offset = vector()
        # support line
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.canvas_data = {}
        self.last_selected_cell = None
        self.selection_index = 'x'

        self.playing = True
        self.flag_playing = True

        #check enter
        self.alert_displayed = False

    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin
        if distance_to_origin.x > 0:
            col = int(distance_to_origin.x / TILE_SIZE)
        else:
            col = int(distance_to_origin.x / TILE_SIZE) - 1

        if distance_to_origin.y > 0:
            row = int(distance_to_origin.y / TILE_SIZE)
        else:
            row = int(distance_to_origin.y / TILE_SIZE) - 1

        return col, row

    def event_loop(self, event):
        self.pan_input(event)

    def pan_input(self, event):
        # kéo chuột phải
        if event.type == pygame.locals.MOUSEBUTTONDOWN and mouse_button()[2]:
            self.pain_active = True
            self.pain_offset = vector(mouse_pos()) - self.origin

        if not mouse_button()[2]:
            self.pain_active = False
        #
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
        # paiing update
        if self.pain_active:
            self.origin = vector(mouse_pos()) - self.pain_offset
        
        #bấm enter để chơi lại
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Xóa bảng chơi và bắt đầu trò chơi mới
                if self.alert_displayed:
                    self.canvas_data.clear()
                    self.playing = True
                    self.flag_playing = True
                    self.selection_index = 'x'
                    self.last_selected_cell = None
                    self.alert_displayed = False
                    sound_track.play(-1)
                return
            elif event.type == pygame.QUIT:
                # Kết thúc trò chơi nếu người chơi tắt cửa sổ
                self.playing = False
                return

    def draw_board(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE
        # lặp vô hạn
        offset_vector = vector(
            x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
        )
        self.support_line_surf.fill('white')
        for col in range(cols + 1):
            x = offset_vector.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR,
                             (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows + 1):
            y = offset_vector.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR,
                             (0, y), (WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surf, (0, 0))

    def left_mouse_click(self, x, y):
        if (x, y) != self.last_selected_cell:
            if (x, y) not in self.canvas_data:
                self.canvas_data[(x, y)] = CanvasTile(self.selection_index)
                if self.selection_index == 'x':
                    game_sounds.play(tick_sound_x)
                else:
                    game_sounds.play(tick_sound_o)
            else:
                return False
            self.last_selected_cell = (x, y)
            self.selection_index = self.canvas_data[(x, y)].get_not_cell()
            if self.check_win((x, y)):
                self.playing = False
                self.alert_winning((x, y))
            return True
        return False

    def draw(self):
        for pos, item in self.canvas_data.items():
            if pos == self.last_selected_cell:
                border_color = (255, 0, 0)
                surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surface.fill((255, 255, 255))
                pygame.draw.rect(surface, border_color,
                                 (0, 0, TILE_SIZE, TILE_SIZE), 2)
                self.display_surface.blit(
                    surface, self.origin + vector(pos) * TILE_SIZE)
            current_pos = self.origin + \
                vector(pos) * TILE_SIZE + vector(TILE_SIZE/8, TILE_SIZE/8)
            if item.has_x:
                image = pygame.image.load(EDITOR_DATA[0]['image'])
                self.display_surface.blit(image, current_pos)
            if item.has_o:
                image = pygame.image.load(EDITOR_DATA[1]['image'])
                self.display_surface.blit(image, current_pos)

    def check_neighbors_cell(self, new_cell, current_index):
        if new_cell not in self.canvas_data:
            return False
        if self.canvas_data[new_cell].get_cell() != current_index:
            return False
        return True

    # theo hàng dọc
    def check_winning_vertical(self, current_cell):
        if current_cell not in self.canvas_data: return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check top
        neighbor_row_start = current_cell[1] - 1
        new_cell = (current_cell[0],neighbor_row_start)
        while neighbor_row_start >= current_cell[1] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row_start -= 1
            check_flag += 1
            new_cell = (current_cell[0],neighbor_row_start)

        #check right
        neighbor_row_end = current_cell[1] + 1
        new_cell = (current_cell[0],neighbor_row_end)
        while neighbor_row_end <= current_cell[1] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row_end += 1
            check_flag += 1
            new_cell = (current_cell[0],neighbor_row_end)

        if check_flag == 5:
            self.draw_player_winning_vertical(neighbor_row_start,neighbor_row_end -1)
            return True
        return False
    
    #check theo hàng ngàng
    def check_winning_horizontal(self, current_cell):
        if current_cell not in self.canvas_data: return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check left
        neighbor_col_start = current_cell[0] - 1
        new_cell = (neighbor_col_start, current_cell[1])
        while neighbor_col_start >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col_start -= 1
            check_flag += 1
            new_cell = (neighbor_col_start, current_cell[1])

        #check right
        neighbor_col_end = current_cell[0] + 1
        new_cell = (neighbor_col_end, current_cell[1])
        while neighbor_col_end <= current_cell[0] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col_end += 1
            check_flag += 1
            new_cell = (neighbor_col_end, current_cell[1])

        if check_flag == 5:
            self.draw_player_winning_horizontal(neighbor_col_start,neighbor_col_end -1)
            return True
        return False

    #đường chéo chính
    def check_winning_main_diagonal(self, current_cell):
        if current_cell not in self.canvas_data: return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1
        # Check top left
        neighbor_col = current_cell[0] - 1
        neighbor_row = current_cell[1] - 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col >= current_cell[0] - 4:
            if check_flag == 5 or not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row -= 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        new_cell_start = new_cell
        #check down right
        neighbor_col = current_cell[0] + 1
        neighbor_row = current_cell[1] + 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col <= current_cell[0] + 4:
            if check_flag == 5 or not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col += 1
            neighbor_row += 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)
        new_cell_end = new_cell

        if check_flag == 5:
            print(f'Start: {new_cell_start}, End: {new_cell_end} ')
            self.draw_player_winning_main_draw_player_winning_auxiliary_diagonal_diagonal(new_cell_start, new_cell_end - vector(1, 1))
            return True
        return False
    
    #đường chéo phụ
    def check_winning_auxiliary_diagonal(self, current_cell):
        if current_cell not in self.canvas_data: return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check top left
        neighbor_col = current_cell[0] - 1
        neighbor_row = current_cell[1] + 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col >= current_cell[0] - 4:
            if check_flag == 5 or not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row += 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)
        new_cell_start = new_cell
        #check down right
        neighbor_col = current_cell[0] + 1
        neighbor_row = current_cell[1] - 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col <= current_cell[0] + 4:
            if check_flag == 5 or not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col += 1
            neighbor_row -= 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)
        new_cell_end = new_cell
        if check_flag == 5:
            print(f'Start: {new_cell_start}, End: {new_cell_end} ')
            self.draw_player_winning_main_draw_player_winning_auxiliary_diagonal_diagonal(new_cell_start - vector(0, 1), new_cell_end - vector(1, 0))
            return True
        return False

    #vẽ hàng ngang
    def draw_player_winning_horizontal(self, start_point, end_point):
        start_pos = self.origin + vector(start_point, self.last_selected_cell[1]) * TILE_SIZE + vector(TILE_SIZE, TILE_SIZE/2)
        end_pos = self.origin + vector(end_point, self.last_selected_cell[1]) * TILE_SIZE + vector(TILE_SIZE, TILE_SIZE/2)
        pygame.draw.line(self.display_surface, (255, 0, 0), start_pos, end_pos, 3)
    
    #vẽ hàng dọc
    def draw_player_winning_vertical(self, start_point, end_point):
        start_pos = self.origin + vector(self.last_selected_cell[0], start_point) * TILE_SIZE + vector(TILE_SIZE/2, TILE_SIZE)
        end_pos = self.origin + vector(self.last_selected_cell[0], end_point) * TILE_SIZE + vector(TILE_SIZE/2, TILE_SIZE)
        pygame.draw.line(self.display_surface, (255, 0, 0), start_pos, end_pos, 3)
    
    # vẽ đường chéo chính , đường chéo phụ
    def draw_player_winning_main_draw_player_winning_auxiliary_diagonal_diagonal(self, start_point, end_point):
        start_pos = self.origin + vector(start_point[0], start_point[1]) * TILE_SIZE + vector(TILE_SIZE, TILE_SIZE)
        end_pos = self.origin + vector(end_point[0], end_point[1]) * TILE_SIZE + vector(TILE_SIZE, TILE_SIZE)
        pygame.draw.line(self.display_surface, (255, 0, 0), start_pos, end_pos, 3)

    def check_win(self, current_cell):
        if self.check_winning_horizontal(current_cell) or self.check_winning_vertical(current_cell) or self.check_winning_main_diagonal(current_cell) or self.check_winning_auxiliary_diagonal(current_cell):
            # print(f"Player wins!")
            return True
        return False

    def alert_winning(self, current_cell):
        self.alert_displayed = True
        _str = ''
        if self.canvas_data[current_cell].get_cell() == 'x':
            _str = f'Player {self.username} wins! Enter to Play again .'
        else:
            _str = f'Player {self.username} wins! Enter to Play again .'

        font = pygame.font.Font(None, 36)
        text = font.render(_str, 1, (255,255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        # Draw border around text
        border_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self.display_surface, (0, 0, 0, 0.5), border_rect)

        # Draw text
        self.display_surface.blit(text, text_rect)

    def run(self):
        if self.flag_playing:
            self.draw_board()
            self.draw()
            # pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
            if not pygame.mixer.get_busy():
                sound_track.play(-1)
            if self.check_win(self.last_selected_cell):
                self.playing = False
                self.alert_winning(self.last_selected_cell)
                #music
                draw_win.play()
                sound_track.stop()
            if not self.playing:
                self.flag_playing = False


class CanvasTile:
    def __init__(self, id):
        self.has_x = False
        self.has_o = False
        self.add_id(id)

    def get_cell(self):
        if self.has_x:
            return 'x'
        else:
            return 'o'

    def get_not_cell(self):
        if self.has_o:
            return 'x'
        else:
            return 'o'

    def add_id(self, id):
        if id == EDITOR_DATA[0]['id']:
            self.has_x = True
        elif id == EDITOR_DATA[1]['id']:
            self.has_o = True
