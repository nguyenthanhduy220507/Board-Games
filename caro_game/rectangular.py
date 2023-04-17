class Square:
    x1= 0
    y1 = 0
    x2 = 0
    y2 = 0
    maunen = "white"
    duongvien = "black"
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2= 0, maunen = "white", duongvien = "black"):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.duongvien = duongvien
        self.maunen = maunen
    def vehinh (self, cas):
        self.hinh = cas.create_rectangle(self.x1,self.y1,self.x2,self.y2,outline = self.duongvien,fill = self.maunen)

    #kiểm tra ô trong bàn cờ trống
    def check_input_mouse(self, x, y):
        if x > self.x1 and x < self.x2 and y > self.y1 and y <self.y2:
            return 1
        else:
            return 0
