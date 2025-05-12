import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen


class GameScreen(BaseScreen):
    def __init__(self, parent_frame, M, N, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)

        self.M, self.N = M, N
        self.cell_size = 40
        self.board = [[0] * N for _ in range(M)]
        ctk.CTkLabel(
            self,
            text=f"Game Mode: {game_mode}",
            font=ctk.CTkFont("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=20)

        # Canvas setup
        w = N * self.cell_size +5
        h = M * self.cell_size +5

        self.canvas = tk.Canvas(self, bg="#363e47", width=w, height=h, highlightthickness=0)
        self.canvas.pack()
        self.draw_grid()
        #left click
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_grid(self):
        for i in range(self.M):
            y =  i * self.cell_size
            x1 = 0
            x2 = self.cell_size * (self.N - 1)
            self.canvas.create_line(x1, y, x2, y, fill="#b7d2f1")

        for j in range(self.N):
            x = j * self.cell_size
            y1 = 0
            y2 = self.cell_size * (self.M - 1)
            self.canvas.create_line(x, y1, x, y2, fill="#ECEFCA")

    def on_click(self, event):
        col = round((event.x) / self.cell_size)
        row = round((event.y) / self.cell_size)

        #validate
        if 0 <= row < self.M and 0 <= col < self.N and self.board[row][col] == 0:
            self.board[row][col] = 1
            self.draw_point(row, col, "white")

    def draw_point(self, row, col, color):
        x = col * self.cell_size
        y = row * self.cell_size
        r = int(self.cell_size / 2) - 6
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = color, outline="black")
