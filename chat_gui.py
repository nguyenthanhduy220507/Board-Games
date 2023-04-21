import customtkinter as ctk
import pyautogui

class GUI:
    def __init__(self, connection, name = 'Player'):
        self.connection = connection
        self.name = name

        self.window = ctk.CTk()
        self.window.title("Chat")
        screen_width, screen_height = pyautogui.size()
        print((screen_width, screen_height))
        # set the dimensions of the window and its position
        self.window.geometry(f'320x250+{(screen_width + 640)//2}+{(screen_height - 640)//2}')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame = ctk.CTkFrame(master=self.window)
        self.frame.pack(fill='both')
        self.message_list = ctk.CTkTextbox(master=self.frame, width=400, state='disabled')
        self.message_list.pack(fill='both', padx=10, pady=(10,0))

        self.entry_field = ctk.CTkEntry(self.frame, placeholder_text='Chat here')
        self.entry_field.bind('<Return>', self.send_message)
        self.entry_field.pack(fill='both', padx=10, pady=10)

    def on_closing(self, after_ids=None):
        if after_ids is not None:
            for id in after_ids:
                self.window.after_cancel(id)
        self.window.destroy()

    def add_message(self, message):
        self.message_list.configure(state='normal')
        self.message_list.insert('end', message)
        self.message_list.configure(state='disabled')
        self.message_list.see('end')

    def send_message(self, event=None):
        message = self.entry_field.get()
        if not message: return
        self.add_message(f"{self.name}: {message}\n")
        self.connection.send(f"Chat:::{self.name}: {message}\n".encode('utf-8'))
        self.entry_field.delete(0, 'end')