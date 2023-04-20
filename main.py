import socket
import threading

from play_surface import Server
from play_surface import Client

if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")
    if mode == 'server':
        username = input("Enter username: ")
        gui = Server('', 55843, username)
        print(socket.gethostbyname(socket.gethostname()))
        threading.Thread(target=gui.gui.run).start()
    elif mode == 'client':
        host = input("Enter server IP address: ")
        port = int(input("Enter server port: "))
        username = input("Enter username: ")
        gui = Client(host, port, username)
        threading.Thread(target=gui.gui.run).start()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")