import pygame
from caro_game.setting import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE, EDITOR_DATA, LINE_COLOR
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_button
from pygame.mouse import get_pos as mouse_pos


class Editor():
    def __init__(self):
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
            else:
                return
            self.last_selected_cell = (x, y)
            self.selection_index = self.canvas_data[(x, y)].get_not_cell()
            if self.check_win((x, y)):
                self.playing = False
                self.alert_winning((x, y))
        self.draw()

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
        if current_cell not in self.canvas_data:
            return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check top
        neighbor_row = current_cell[1] - 1
        new_cell = (current_cell[0], neighbor_row)
        while neighbor_row >= current_cell[1] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row -= 1
            check_flag += 1
            new_cell = (current_cell[0], neighbor_row)

        # check right
        neighbor_row = current_cell[1] + 1
        new_cell = (current_cell[0], neighbor_row)
        while neighbor_row <= current_cell[1] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row += 1
            check_flag += 1
            new_cell = (current_cell[0], neighbor_row)

        if check_flag == 5:
            return True
        return False
    # check theo hàng ngàng

    def check_winning_horizontal(self, current_cell):
        if current_cell not in self.canvas_data:
            return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check left
        neighbor_col = current_cell[0] - 1
        new_cell = (neighbor_col, current_cell[1])
        while neighbor_col >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            check_flag += 1
            new_cell = (neighbor_col, current_cell[1])

        # check right
        neighbor_col = current_cell[0] + 1
        new_cell = (neighbor_col, current_cell[1])
        while neighbor_col <= current_cell[0] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col += 1
            check_flag += 1
            new_cell = (neighbor_col, current_cell[1])

        if check_flag == 5:
            return True
        return False
    # đường chéo chính

    def check_winning_main_diagonal(self, current_cell):
        if current_cell not in self.canvas_data:
            return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check top left
        neighbor_col = current_cell[0] - 1
        neighbor_row = current_cell[1] - 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row -= 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        # check down right
        neighbor_col = current_cell[0] + 1
        neighbor_row = current_cell[1] + 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col <= current_cell[0] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col += 1
            neighbor_row += 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        if check_flag == 5:
            return True
        return False
    # đường chéo phụ

    def check_winning_auxiliary_diagonal(self, current_cell):
        if current_cell not in self.canvas_data:
            return False
        current_index = self.canvas_data[current_cell].get_cell()
        # print(current_index)
        check_flag = 1

        # Check top left
        neighbor_col = current_cell[0] - 1
        neighbor_row = current_cell[1] + 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row += 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        # check down right
        neighbor_col = current_cell[0] + 1
        neighbor_row = current_cell[1] - 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col <= current_cell[0] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col += 1
            neighbor_row -= 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        if check_flag == 5:
            return True
        return False

    def check_win(self, current_cell):
        if self.check_winning_horizontal(current_cell) or self.check_winning_vertical(current_cell) or self.check_winning_main_diagonal(current_cell) or self.check_winning_auxiliary_diagonal(current_cell):
            # print(f"Player wins!")
            return True
        return False

    def alert_winning(self, current_cell):
        _str = ''
        if self.canvas_data[current_cell].get_cell() == 'x':
            _str = 'Player X wins!'
        else:
            _str = 'Player O wins!'

        font = pygame.font.Font(None, 36)
        text = font.render(_str, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        # Draw border around text
        border_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self.display_surface, (255, 0, 0), border_rect)

        # Draw text
        self.display_surface.blit(text, text_rect)

    def run(self):
        if self.flag_playing:
            self.draw_board()
            # pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
            if self.check_win(self.last_selected_cell):
                self.playing = False
                self.alert_winning(self.last_selected_cell)
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
