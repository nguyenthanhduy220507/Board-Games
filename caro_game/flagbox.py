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
        if self.giatri == 1: #hình tròn
        # vẽ hình chữ nhật với kích thước =hình tròn
            rect_width = abs(self.x2 - self.x1) 
            rect_height = abs(self.y2 - self.y1) 
            rect_x = self.x1
            rect_y = self.y1
            pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))
            
            width = abs(self.x2 - self.x1)
            height = abs(self.y2 - self.y1)
            radius = min(width, height) // 2
            center = (self.x1 + width // 2, self.y1 + height // 2)
            pygame.draw.circle(screen, (119, 192, 74), center, radius)

        if self.giatri == -1: # hình square
            # vẽ hình chữ nhật với kích thước = hình vuông
            rect_width = abs(self.x2 - self.x1)
            rect_height = abs(self.y2 - self.y1) 
            rect_x = self.x1
            rect_y = self.y1 
            pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))
            
            pygame.draw.line(screen, (255, 0, 0), (self.x1, self.y1 ), (self.x2 , self.y2 ), 3)
            pygame.draw.line(screen, (255, 0, 0), (self.x2, self.y1 ), (self.x1 , self.y2 ), 3)

