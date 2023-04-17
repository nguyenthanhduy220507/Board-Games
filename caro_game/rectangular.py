import pygame

class Square:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    maunen = (255, 255, 255) # màu nền mặc định là trắng
    duongvien = (0, 0, 0) # màu đường viền mặc định là đen

    def __init__(self, x1=0, y1=0, x2=0, y2=0, maunen=(255, 255, 255), duongvien=(0, 0, 0)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.duongvien = duongvien
        self.maunen = maunen

    def vehinh(self, screen):
        pygame.draw.rect(screen, self.maunen, (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
        pygame.draw.rect(screen, self.duongvien, (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1), 1)

    # kiểm tra ô trong bàn cờ trống
    def check_input_mouse(self, x, y):
        if x > self.x1 and x < self.x2 and y > self.y1 and y < self.y2:
            return 1
        else:
            return 0
