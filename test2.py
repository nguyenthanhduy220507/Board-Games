import sys
import tkinter as tk
import pygame

# Khởi tạo cửa sổ Tkinter
root = tk.Tk()
root.geometry("400x400")

# Khởi tạo bề mặt Pygame
pygame.init()
pygame.display.set_mode((640, 640))

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Vẽ đối tượng Pygame
    pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (0, 0, 50, 50))
    pygame.display.update()
    
    # Cập nhật giao diện Tkinter
    root.update()