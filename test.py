import threading
import tkinter as tk

def gui_thread():
    # Tạo GUI Tkinter tại đây
    root = tk.Tk()
    root.mainloop()

def main():
    # Tạo thread phụ để chạy GUI
    gui = threading.Thread(target=gui_thread)
    gui.start()

    # Chạy vòng lặp chính của Tkinter
    root = tk.Tk()
    root.mainloop()

if __name__ == '__main__':
    main()
