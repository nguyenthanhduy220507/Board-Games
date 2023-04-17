import socket

from chat_gui import ChatGUI


if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")

    if mode == 'server':
        username = input("Enter username: ")
        chatGUI = ChatGUI('', 55843, username)
        print(socket.gethostbyname(socket.gethostname()))
        chatGUI.start_server()
    elif mode == 'client':
        host = input("Enter server IP address: ")
        port = int(input("Enter server port: "))
        username = input("Enter username: ")
        chatGUI = ChatGUI(host, port, username)
        chatGUI.start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")