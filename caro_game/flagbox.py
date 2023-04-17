from caro_game.rectangular import *
import pygame

class FlagBox(Square):
    giatri =0 # gia tri = 1 lã O , gia tri = -1 là X
    def __init__(self,mx1,my1,mx2,my2):
        super().__init__(mx1,my1,mx2,my2)
        self.giatri = 0
    
    # vẽ sự kiên X O
    def vehinh(self,screen):
        super().vehinh(screen)
        dx = (self.x2 - self.x1)/4 # độ dài của cạnh /4
        dy = (self.y2 - self.y1)/4
        if self.giatri == 1: #hình tròn
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x1 + dx,self.y1 + dy, self.x2-dx, self.y2 -dy))
        if self.giatri == -1: # hình square
            pygame.draw.line(screen, (255, 255, 255), (self.x1+dx, self.y1 +dy), (self.x2 -dx, self.y2 -dy), 10)
            pygame.draw.line(screen, (255, 255, 255), (self.x2-dx, self.y1 +dy), (self.x1 +dx, self.y2 -dy), 10)
