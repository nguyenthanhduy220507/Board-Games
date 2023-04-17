from Oc import *
class BanCo:
    player = 1
    winning = 0
    condition = 0
    arr = []
    value_x_first = 30 #gia tri x dau
    value_y_first = 30 # gia tri y dau
    value_length_arr_2 = 30 # độ dài
    def __init__(self):
        for i in range(0,20):
            line = []
            for j in range(0,20):
                mx = self.value_x_first + j * self.value_length_arr_2
                my = self.value_y_first + i * self.value_length_arr_2
                line.append(Oc(mx, my, mx + self.value_length_arr_2, my + self.value_length_arr_2))
            self.arr.append(line)

    #vẽ số dòng và cột 
    def vehinh(self,cas):
        for i in range(0,20):
            for j in range(0,20):
                self.arr[i][j].vehinh(cas)

    #thực hiện click_Mouse
    def click_flag_box(self, cas, x, y):
        if self.condition == 0:
            return
        for i in range(0,20):
            for j in range(0,20):
                if self.arr[i][j].check_input_mouse(x,y) ==1 and self.arr[i][j].giatri == 0: # kiểm tra ô ch được bấm và giatri = 0 
                    self.arr[i][j].giatri = self.player
                    self.arr[i][j].vehinh(cas)
                    if self.check_winning(i,j) == 1:
                        self.condition = 0
                        self.alert_wining(cas)
                    else:
                        self.player = self.player * -1 # đổi chiều người chơi


    def check_winning(self, mi, mj):
        if self.check_winning_vertical(mi, mj) == 1:
            return 1
        else:
            return 0
    
    #check theo chiều dọc
    def check_winning_vertical(self, mi, mj):
        count = 0
        #doc trên
        i = mi -1
        j = mj
        if i < 0:
            i = 0
        while i>=0:
            if self.arr[i][j].giatri == self.player:
                count+=1
            else:
                break
            i = i-1
        #doc duoi
        i = mi + 1
        j = mj
        while i <= 20:
            if self.arr[i][j].giatri == self.player:
                count+=1
            else:
                break
            i = i+1
        
        #check count
        if count >=4:
            return 1
        else:
            return 0


    def alert_wining(self,cas):
        str = "PLayer "
        if self.player == -1:
            str += "X Winner!!!"
        else:
            str += "O Winner!!!"
        cas.create_text(100,10,fill="darkblue",font="Times 15 italic bold", text = str)