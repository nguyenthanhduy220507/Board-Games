import pygame
import sys
from setting import *
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_button
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load


class Editor():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = vector()
        self.pain_active = False
        self.pain_offset = vector()
        self.current_player = cross_player
        # support line
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
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

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            if self.playing:
                self.canvas_add(event)

    def pan_input(self, event):
        #kéo chuột phải
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_button()[2]:
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

        self.display_surface.blit(self.support_line_surf,(0,0))

    def canvas_add(self, event):
        if mouse_button()[0] and event.type == pygame.MOUSEBUTTONDOWN:
            current_cell = self.get_current_cell()
            if current_cell != self.last_selected_cell:
                if current_cell not in self.canvas_data:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                else:
                    return
                self.last_selected_cell = current_cell
                self.selection_index = self.canvas_data[current_cell].get_not_cell()
                if self.check_win(current_cell):
                    self.playing = False
                    self.alert_winning(current_cell)
                

    def draw(self):
        for pos, item in self.canvas_data.items():
            if pos == self.last_selected_cell:
                border_color = (255, 0, 0)
                surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surface.fill((255,255,255))
                pygame.draw.rect(surface, border_color, (0, 0, TILE_SIZE,TILE_SIZE), 2)
                self.display_surface.blit(surface, self.origin + vector(pos) * TILE_SIZE)
            current_pos = self.origin + vector(pos) * TILE_SIZE + vector(TILE_SIZE/8, TILE_SIZE/8)
            if item.has_x:
                image = pygame.image.load(EDITOR_DATA[0]['image'])
                self.display_surface.blit(image, current_pos)


            if item.has_o:
                image = pygame.image.load(EDITOR_DATA[1]['image'])
                self.display_surface.blit(image, current_pos)

    def check_neighbors_cell(self,new_cell, current_index):
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
        neighbor_row = current_cell[1] - 1
        new_cell = (current_cell[0],neighbor_row)
        while neighbor_row >= current_cell[1] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row -= 1
            check_flag += 1
            new_cell = (current_cell[0],neighbor_row)

        #check right
        neighbor_row = current_cell[1] + 1
        new_cell = (current_cell[0],neighbor_row)
        while neighbor_row <= current_cell[1] + 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_row += 1
            check_flag += 1
            new_cell = (current_cell[0],neighbor_row)

        if check_flag == 5:
            return True
        return False
    #check theo hàng ngàng
    def check_winning_horizontal(self, current_cell):
        if current_cell not in self.canvas_data: return False
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

        #check right
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
        while neighbor_col >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row -= 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        #check down right
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
        while neighbor_col >= current_cell[0] - 4 and check_flag != 5:
            if not self.check_neighbors_cell(new_cell, current_index):
                break
            neighbor_col -= 1
            neighbor_row += 1
            check_flag += 1
            new_cell = (neighbor_col, neighbor_row)

        #check down right
        neighbor_col = current_cell[0] + 1
        neighbor_row = current_cell[1] - 1
        new_cell = (neighbor_col, neighbor_row)
        while neighbor_col <= current_cell[0] + 4  and check_flag != 5:
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
        str = ''
        if self.canvas_data[current_cell].get_cell() == 'x':
            str = 'Player X wins!'
        else:
            str = 'Player O wins!'
        
        font = pygame.font.Font(None, 36)
        text = font.render(str, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        # Draw border around text
        border_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self.display_surface, (255, 0, 0), border_rect)

        # Draw text
        self.display_surface.blit(text, text_rect)


    
    # def get_cell_index(self, pos):
    #     # tính toán vị trí của ô trên ma trận
    #     x = int((pos.x - self.origin.x) // TILE_SIZE)
    #     y = int((pos.y - self.origin.y) // TILE_SIZE)
    #     # tính toán chỉ số của hàng và cột tương ứng với ô được chọn
    #     row = y
    #     col = x
    #     return row, col

    # vẽ bằng pygame
    # def draw_shape(self, pos):
        if self.current_player == cross_player:  # hình X
            x = int((pos.x - self.origin.x) // TILE_SIZE) * \
                TILE_SIZE + self.origin.x
            y = int((pos.y - self.origin.y) // TILE_SIZE) * \
                TILE_SIZE + self.origin.y
            pygame.draw.line(self.display_surface, 'red', (x, y),
                             (x + TILE_SIZE, y + TILE_SIZE), 2)
            pygame.draw.line(self.display_surface, 'red',
                             (x + TILE_SIZE, y), (x, y + TILE_SIZE), 2)
            print("4")
        elif self.current_player == circle_player:  # hình O
            x = int((pos.x - self.origin.x) // TILE_SIZE) * \
                TILE_SIZE + self.origin.x + TILE_SIZE // 2
            y = int((pos.y - self.origin.y) // TILE_SIZE) * \
                TILE_SIZE + self.origin.y + TILE_SIZE // 2
            radius = TILE_SIZE // 2 - 2
            pygame.draw.circle(self.display_surface, 'cyan', (x, y), radius, 2)
            print("3")

    # def on_mouse_button_down(self):
        # tính toán vị trí của ô trên ma trận
        pos = vector(pygame.mouse.get_pos())

        cell_index = self.get_cell_index(pos)
        row, col = cell_index
        print("Selected cell:", row, col)
        if self.current_player == cross_player:
            self.current_player = circle_player

            print("2")
        elif self.current_player == circle_player:
            self.current_player = cross_player
        self.draw_shape(pos)
        print("1")

    def run(self, dt):
        self.event_loop()
        # self.display_surface.fill("white")
        if self.flag_playing:
            self.draw_board()
            self.draw()
            pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
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
        if id == EDITOR_DATA[0]['id']: self.has_x = True
        elif id == EDITOR_DATA[1]['id']: self.has_o = True

