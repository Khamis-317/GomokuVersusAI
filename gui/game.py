import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, parent_frame, N, M, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.parent_frame = parent_frame
        self.M = M #col
        self.N = N #row
        self.cell_size = 40
        self.board = []
        self.margin = 20
        self.game_started = False
        self.turn = 1
        self.game_mode = game_mode
        for i in range(M):
            row = [0] * N
            self.board.append(row)

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
            command=self.back_to_menu,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.back_button.grid(row=0, column=0, padx=10)

        #Start Button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start",
            command=self.start_game,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.start_button.grid(row=0, column=1, padx=10)

        #Reset Button
        self.reset_button= ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset_game,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        #Canvas setup
        w = N * self.cell_size  + self.margin * 2
        h = M * self.cell_size  + self.margin * 2

        self.canvas = tk.Canvas(self, bg="#363e47", width=w, height=h, highlightthickness=0)
        self.canvas.pack()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click) #catch left click on canvas

        #Players
        if game_mode == "AI vs AI":
            self.ai_player1 = "Minimax" #Going to change
            self.ai_player2 = "Alpha Beta Pruning" #Going to change
        else:
            self.human_player = "" #No need for change
            self.ai_player = "Minimax" #Going to change

    def click(self, event):
        col = round((event.x) / self.cell_size)
        row = round((event.y) / self.cell_size)
        if self.game_started and self.game_mode == "Human vs AI" and self.turn == 1:
            self.add_point(row, col, "black")
            if not self.check_win():
                self.turn = 2
                self.after(300, self.ai_move)
        else:
            pass #flagging win


    def ai_move(self):
        if not self.game_started:
            return 0
        if self.turn == 1:
            row, col = self.dummy() #replace by alpha beta get move <<<<
        else:
            row, col = self.dummy() #replace by minmax get move <<<<<

        color = "white" if self.turn == 1 else "red"
        self.add_point(row, col, color)

        if not self.check_win():
            self.turn = 1 if self.turn == 2 else 2 #At human vs. ai mode this line behaves the same as turn = 1(human)
            if self.game_mode == "AI vs AI":
                self.after(300, self.ai_move) #recurse with another AI algo
        else:
            pass #flagging win

    def start_game(self):
        self.game_started = True
        self.start_button.configure(state="disabled")
        self.reset_button.configure(state="enabled")
        self.back_button.configure(state="disabled")
        if (self.game_mode == "AI vs AI"): #only in Ai mode otherwise click event is the orchestrator
            self.ai_move()

    def reset_game(self):
        self.game_started = False
        self.start_button.configure(state="normal")
        for i in range(self.M):
            for j in range(self.N):
                self.board[i][j] = 0
        self.canvas.delete("all")
        self.draw_grid()
        self.turn = 1
        self.back_button.configure(state="normal")
        self.reset_button.configure(state="disabled")

    def back_to_menu(self):
        from gui.start_menu import StartMenu
        self.destroy()
        start_menu = StartMenu(self.parent_frame)
        start_menu.show()


    def check_win(self):
        pass

    # Canvas Drawing

    def add_point(self, row, col, color):
        if 0 <= row < self.M and 0 <= col < self.N and self.board[row][col] == 0:
            self.board[row][col] = 1 if self.turn == 1 else 2
            self.draw_point(row, col, color)

    def draw_point(self, row, col, color):
        x = self.margin + (col * self.cell_size)
        y = self.margin + (row * self.cell_size)
        r = int(self.cell_size / 2) - 6
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black")

    def draw_grid(self):
        for i in range(self.M):
            y = self.margin + (i * self.cell_size)
            x1 = self.margin
            x2 = self.cell_size * (self.N - 1) + self.margin
            self.canvas.create_line(x1, y, x2, y, fill="#b7d2f1")

        for j in range(self.N):
            x = self.margin + (j * self.cell_size)
            y1 = self.margin
            y2 = self.cell_size * (self.M - 1) + self.margin
            self.canvas.create_line(x, y1, x, y2, fill="#b7d2f1")


    #Temp Function
    def dummy(self):
        for row in range(self.M):
            for col in range(self.N):
                if self.board[row][col] == 0:
                    return row, col