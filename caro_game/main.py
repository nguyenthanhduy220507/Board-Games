from tkinter import *
from caro_game.board import *


class Caro:
    def __init__(self, connection):
        self.connection = connection
        self.window = Tk()
        self.window.title("Caro")
        
        self.cas = Canvas(self.window, height=640, width=640)
        self.cas.pack()

        self.banco = Board()
        self.banco.vehinh(self.cas)
        self.banco.condition = 1

        self.cas.bind_all('<Button-1>', self.click_mouse_button)

    def clicked(self, x, y):
        self.banco.click_flag_box(self.cas, x, y)

    def click_mouse_button(self, event):
        self.clicked(event.x, event.y)
        self.connection.send(f'{event.x},{event.y}'.encode('utf-8'))
