import socket
import customtkinter as ctk
from threading import Thread

class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.gui = GUI(self.sock, self.username)

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
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()

        self.gui = GUI(self.conn, self.username)

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
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

        self.window = ctk.CTk()
        self.window.title("Chat")

        self.message_list = ctk.CTkTextbox(master=self.window, width=400, state="disabled")
        self.message_list.pack(fill='both')

        self.entry_field = ctk.CTkEntry(self.window, placeholder_text='Chat here')
        self.entry_field.bind('<Return>', self.send_message)
        self.entry_field.pack(fill='both', pady=10)

    def add_message(self, message):
        self.message_list.insert(ctk.END, message)

    def send_message(self, event=None):
        message = self.entry_field.get()
        if not message: return
        self.add_message(f"{self.name}: {message}\n")
        self.connection.send(f"{self.name}: {message}\n".encode('utf-8'))
        self.entry_field.delete(0, 'end')

class ChatGUI:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

    def start_client(self):
        client = Client(self.host, self.port, self.username)
        client.gui.window.mainloop()

    def start_server(self):
        server = Server(self.host, self.port, self.username)
        server.gui.window.mainloop()