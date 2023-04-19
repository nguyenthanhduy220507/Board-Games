import socket
import threading
import customtkinter

from chat_gui import ChatGUI
from game_gui import GameGUI

class MainMenu(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("250x180")
        self.title("Board Game")

        self.label = customtkinter.CTkLabel(master=self, text="Select game:")
        self.label.pack()

        self.game_menu = customtkinter.CTkOptionMenu(master=self, values=["Caro"], command=None)
        self.game_menu.pack(padx=10, pady=(5, 15))

        self.start_server = customtkinter.CTkButton(master=self, text='Create Server', command=self.open_start_server_window)
        self.start_server.pack(padx=10, pady=5)

        self.join_server = customtkinter.CTkButton(master=self, text='Join Server', command=None)
        self.join_server.pack(padx=10, pady=5)

        self.start_server_window = None

    def open_start_server_window(self):
        dialog = customtkinter.CTkInputDialog(text="Input username:", title="Create Server")
        print("Number:", dialog.get_input())
        chatGUI = ChatGUI('', 55843, dialog.get_input())
        gameGUI = GameGUI('', 55844)
        self.destroy()
        print(socket.gethostbyname(socket.gethostname()))
        threading.Thread(target=chatGUI.start_server).start()
        threading.Thread(target=gameGUI.start_server).start()


class StartServer(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(master=self, text="Server config")
        self.label.pack(padx=10, pady=10)

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="Input username")
        self.entry.pack(padx=10, pady=(10, 5))

        self.start_server = customtkinter.CTkButton(master=self, text='Create Server', command=None)
        self.start_server.pack(padx=10, pady=5)


class StartClient(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

if __name__ == "__main__":
    MainMenu().mainloop()
    mode = input("Enter 'server' or 'client' to start: ")
    if mode == 'server':
        username = input("Enter username: ")
        # chatGUI = ChatGUI('', 55843, username)
        # gameGUI = GameGUI('', 55844)
        # print(socket.gethostbyname(socket.gethostname()))
        # threading.Thread(target=chatGUI.start_server).start()
        # threading.Thread(target=gameGUI.start_server).start()
    elif mode == 'client':
        host = input("Enter server IP address: ")
        port = int(input("Enter server port: "))
        username = input("Enter username: ")
        chatGUI = ChatGUI(host, port, username)
        gameGUI = GameGUI(host, port + 1)
        threading.Thread(target=chatGUI.start_client).start()
        threading.Thread(target=gameGUI.start_client).start()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")