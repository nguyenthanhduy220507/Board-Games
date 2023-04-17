from caro_game.rectangular import Square
import pygame

class FlagBox(Square):
    giatri =0 # gia tri = 1 lã O , gia tri = -1 là X
    def __init__(self,mx1,my1,mx2,my2):
        super().__init__(mx1,my1,mx2,my2)
        self.giatri = 0
    
    # vẽ sự kiên X O
    def vehinh(self,screen):
        super().vehinh(screen)
        # dx = (self.x2 - self.x1)/4 # độ dài của cạnh /4
        # dy = (self.y2 - self.y1)/4
        if self.giatri == 1: #hình tròn
                width = abs(self.x2 - self.x1)
                height = abs(self.y2 - self.y1)
                radius = min(width, height) // 2
                center = (self.x1 + width // 2, self.y1 + height // 2)
                pygame.draw.circle(screen, (119, 192, 74), center, radius)
        if self.giatri == -1: # hình square
            pygame.draw.line(screen, (255, 0, 0), (self.x1, self.y1 ), (self.x2 , self.y2 ), 3)
            pygame.draw.line(screen, (255, 0, 0), (self.x2, self.y1 ), (self.x1 , self.y2 ), 3)
