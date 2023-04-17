from caro_game.rectangular import Square
import pygame

class FlagBox(Square):
    giatri =0 # gia tri = 1 lã O , gia tri = -1 là X
    def __init__(self,mx1,my1,mx2,my2):
        super().__init__(mx1,my1,mx2,my2)
        self.giatri = 0
    
    def vehinh(self, screen):
        super().vehinh(screen)
        dx = self.square_size / 4 # độ dài của cạnh /4
        dy = self.square_size / 4
        if self.giatri == 1: # hình tròn
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + dx, self.y + dy, self.square_size - 2 * dx, self.square_size - 2 * dy))
        if self.giatri == -1: # hình vuông
            pygame.draw.line(screen, (255, 255, 255), (self.x + dx, self.y + dy), (self.x + self.square_size - dx, self.y + self.square_size - dy), 10)
            pygame.draw.line(screen, (255, 255, 255), (self.x + self.square_size - dx, self.y + dy), (self.x + dx, self.y + self.square_size - dy), 10)

