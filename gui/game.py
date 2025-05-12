import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen


class GameScreen(BaseScreen):
    def __init__(self, parent_frame, M, N, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)

        self.M, self.N = M, N
        self.cell_size = 40
        self.board = [[0] * N for _ in range(M)]
        self.game_started = False
        self.turn = 1
        #Title
        ctk.CTkLabel(
            self,
            text=f"Game Mode: {game_mode}",
            font=ctk.CTkFont("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=20)

        #buttons
        button_frame = ctk.CTkFrame(self, fg_color="#363e47")
        button_frame.pack(pady=20)
        # Back Button
        self.back_button = ctk.CTkButton(
            button_frame,
            text="Back",
            command=None,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.back_button.grid(row=0, column=0, padx=10)
        #Start Button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start",
            command=None,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.start_button.grid(row=0, column=1, padx=10)

        #Reset Button
        self.reset_button= ctk.CTkButton(
            button_frame,
            text="Reset",
            command=None,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.reset_button.grid(row=0, column=2, padx=10)





        #Canvas setup
        w = N * self.cell_size +5
        h = M * self.cell_size +5

        self.canvas = tk.Canvas(self, bg="#363e47", width=w, height=h, highlightthickness=0)
        self.canvas.pack()
        self.draw_grid()
        #left click
        self.canvas.bind("<Button-1>", self.click)


        if game_mode == "Ai vs AI":
            self.ai_player1 = "Minimax"
            self.ai_player2 = "Alpha Beta Pruning"
        else:
            self.ai_player = "Minimax"


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
            self.canvas.create_line(x, y1, x, y2, fill="#b7d2f1")

    def click(self, event):
        col = round((event.x) / self.cell_size)
        row = round((event.y) / self.cell_size)
        if self.turn == 1:
            self.add_point(row, col, "red")
        else:
            return

    def add_point(self, row, col, color):
        if 0 <= row < self.M and 0 <= col < self.N and self.board[row][col] == 0:
            self.board[row][col] = 1
            self.draw_point(row, col, color)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
        #check win function call
    def draw_point(self, row, col, color):
        x = col * self.cell_size
        y = row * self.cell_size
        r = int(self.cell_size / 2) - 6
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = color, outline="black")
