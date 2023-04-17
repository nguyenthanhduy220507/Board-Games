import socket
import threading

from chat_gui import ChatGUI
from game_gui import GameGUI


if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")

    if mode == 'server':
        username = input("Enter username: ")
        chatGUI = ChatGUI('', 55843, username)
        gameGUI = GameGUI('', 55843)
        print(socket.gethostbyname(socket.gethostname()))
        threading.Thread(target=chatGUI.start_server).start()
        threading.Thread(target=gameGUI.start_server).start()
    elif mode == 'client':
        host = input("Enter server IP address: ")
        port = int(input("Enter server port: "))
        username = input("Enter username: ")
        chatGUI = ChatGUI(host, port, username)
        gameGUI = GameGUI(host, port)
        threading.Thread(target=chatGUI.start_client).start()
        threading.Thread(target=gameGUI.start_client).start()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")