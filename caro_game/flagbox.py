from caro_game.rectangular import *
class FlagBox(Square):
    giatri =0 # gia tri = 1 lã O , gia tri = -1 là X
    def __init__(self,mx1,my1,mx2,my2):
        super().__init__(mx1,my1,mx2,my2)
        self.giatri = 0
    
    # vẽ sự kiên X O
    def vehinh(self,cas):
        super().vehinh(cas)
        dx = (self.x2 - self.x1)/4 # độ dài của cạnh /4
        dy = (self.y2 - self.y1)/4
        if self.giatri == 1: #hình tròn
            cas.create_oval(self.x1 + dx,self.y1 + dy, self.x2-dx, self.y2 -dy)
        if self.giatri == -1: # hình square
            cas.create_line(self.x1+dx, self.y1 +dy, self.x2 -dx, self.y2 -dy)
            cas.create_line(self.x2-dx, self.y1 +dy, self.x1 +dx, self.y2 -dy)