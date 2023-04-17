from tkinter import *
from hcn import *
from banco import *


class Caro:
    def __init__(self, connection):
        self.connection = connection
        self.window = Tk()
        self.window.title("Chat")
        
        self.cas = Canvas(self.window, height=640, width=640)
        self.cas.pack()

        self.banco = BanCo()
        self.banco.vehinh(self.cas)
        self.banco.condition = 1
        self.h1 = Hcn(50,50, 250,150)

        self.cas.bind_all('<Button-1>', self.click_mouse_button)

    def clicked(self, x, y):
        self.banco.click_flag_box(self.cas, x, y)

    def click_mouse_button(self, event):
        self.clicked(event.x, event.y)
        self.connection.send(f'{event.x},{event.y}'.encode('utf-8'))
