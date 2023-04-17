import socket
import tkinter as tk
from threading import Thread

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.gui = GUI(self.sock)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                self.gui.add_message(message)
            except OSError:
                break

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()

        self.gui = GUI(self.conn)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode('utf-8')
                self.gui.add_message(message)
            except OSError:
                break

    def send(self, message):
        self.conn.sendall(message.encode('utf-8'))

class GUI:
    def __init__(self, connection):
        self.connection = connection

        self.window = tk.Tk()
        self.window.title("Chat")

        self.message_frame = tk.Frame(self.window)
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.message_list = tk.Listbox(self.message_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.message_list.pack()
        self.message_frame.pack()

        self.entry_field = tk.Entry(self.window, width=50)
        self.entry_field.bind('<Return>', self.send_message)
        self.send_button = tk.Button(self.window, text='Send', command=self.send_message)
        self.entry_field.pack()
        self.send_button.pack()

    def add_message(self, message):
        self.message_list.insert(tk.END, message)

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.add_message("You: " + message)
        self.connection.send(message.encode('utf-8'))
        self.entry_field.delete(0, tk.END)

def start_client():
    host = input("Enter server IP address: ")
    port = int(input("Enter server port: "))
    client = Client(host, port)
    client.gui.window.mainloop()

def start_server():
    host = ''
    port = 55843
    server = Server(host, port)
    server.gui.window.mainloop()

if __name__ == "__main__":
    mode = input("Enter 'server' or 'client' to start: ")
    if mode == 'server':
        print(socket.gethostbyname(socket.gethostname()))
        start_server()
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")