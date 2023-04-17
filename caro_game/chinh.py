from tkinter import *
from hcn import *
from banco import *
tk = Tk()
cas = Canvas (tk, height = 640, width = 640)
cas.pack()

banco = BanCo()
banco.vehinh(cas)
banco.condition = 1
#cas.create_rectangle(10,10,200,100,outline="black",fill="green")
h1 = Hcn(50,50, 250,150)
# h1.vehinh(cas)

def click_mouse_button(event):
    banco.click_flag_box(cas,event.x, event.y)


cas.bind_all('<Button-1>', click_mouse_button)

tk.mainloop()