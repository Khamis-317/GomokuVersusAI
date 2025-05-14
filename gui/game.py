import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, parent_frame, ROWS, COLS, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.parent_frame = parent_frame
        self.M = ROWS  # number of rows
        self.N = COLS  # number of cols
        self.cell_size = 40
        self.margin = 20
        self.board = []
        self.round_count = 0
        self.game_started = False
        self.turn = 1
        self.game_mode = game_mode

        for i in range(ROWS):
            row = [0] * COLS
            self.board.append(row)

        #Title
        ctk.CTkLabel(
            self,
            text=f"Game Mode: {game_mode}",
            font=ctk.CTkFont("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=20)


        #winning and draw Labels
        self.winner_label = ctk.CTkLabel(self, fg_color="transparent")
        self.draw_label = ctk.CTkLabel(self, fg_color="transparent")

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
        w = COLS * self.cell_size + self.margin  ##should add margin
        h = ROWS * self.cell_size + self.margin

        self.canvas = tk.Canvas(self, bg="#363e47", width=w, height=h, highlightthickness=0)
        self.canvas.pack()
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.click) #catch left click on canvas

        #Players
        if game_mode == "AI vs AI":
            self.ai_player1 = "Alpha Beta Pruning" #Going to change
            self.ai_player2 = "Minimax" #Going to change
        else:
            self.human_player = "Human" #No need for change
            self.ai_player = "Minimax" #Going to change


    def click(self, event):
        if self.game_started:
            if self.game_mode == "Human vs AI" and self.turn == 1:
                if(self.is_board_full()):
                    self.game_started = False
                col = round((event.x - self.margin) / self.cell_size)
                row = round((event.y - self.margin) / self.cell_size)
                if self.add_point(row, col):
                    self.round_count += 1
                    self.draw_point(row, col, "black")
                    win = self.check_win(row, col)
                    if win is not None:
                        self.game_started = False
                        self.canvas.create_line(win[0][0], win[0][1], win[1][0], win[1][1], fill="yellow", width=5)
                        self.display_winner()
                    else:
                        if (self.is_board_full()):
                            self.game_started = False
                            self.display_draw_message()
                        else:
                            self.turn = 2
                            self.after(300, self.ai_move)
        else:
            print("Game is finished!")


    def ai_move(self):
        if not self.game_started:
            print("Game is finished!")
            return
        if self.turn == 1:
            row, col = self.dummy() #replace by alpha beta get move <<<<
        else:
            row, col = self.dummy() #replace by minmax get move <<<<<

        color = "white" if self.turn == 1 else "red"
        if self.add_point(row, col):
            self.round_count += 1
            self.draw_point(row, col, color)

        win = self.check_win(row, col)
        if win is None:
            if (self.is_board_full()):
                game_started = False
                self.display_draw_message()
            else:
                self.turn = 1 if self.turn == 2 else 2 #At human vs. ai mode this line behaves the same as turn = 1(human)
                if self.game_mode == "AI vs AI":
                    self.after(300, self.ai_move) #recurse with another AI algo
        else:
            self.game_started = False
            self.canvas.create_line(win[0][0], win[0][1], win[1][0], win[1][1], fill="yellow", width=5)
            self.display_winner()

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
        self.winner_label.pack_forget()
        self.draw_label.pack_forget()
        self.back_button.configure(state="normal")
        self.reset_button.configure(state="disabled")
        self.round_count = 0

    def back_to_menu(self):
        from gui.start_menu import StartMenu
        self.destroy()
        start_menu = StartMenu(self.parent_frame)
        start_menu.show()


    def check_win(self, row, col):
        WINNING_SEQ = 5
        dx = [1,0,1,1,0,-1,-1,-1]
        dy = [0,1,1,-1,-1,-1,0,1]
        # check 8 directions
        #(-1,-1) | ( 0,-1) | (+1,-1)
        #(-1, 0) | (row, col) | (+1, 0)
        #(-1, +1) | ( 0, +1) | (-1, +1)
        r = 0
        c = 0
        # check for a wining sequence at each direction around the last played cell
        for dr, dc in zip(dx,dy):
            # skipping the current cell and starting the count at 1
            count = 1
            for i in range(1, 5):
                r,c = row + dr * i , col + dc * i
                if 0 <= r < self.M and 0 <= c < self.N and self.board[r][c] == self.board[row][col]:
                    count += 1
                else:
                    break
            if count == WINNING_SEQ:
                x1 = col * self.cell_size + self.margin
                y1 = row * self.cell_size + self.margin
                x2 = c * self.cell_size + self.margin
                y2 = r * self.cell_size + self.margin
                # return the start and end of the winning sequence
                return ((x1, y1), (x2, y2))
        return None

    def is_board_full(self):
        return self.round_count == self.M*self.N
    # Canvas Drawing

    def add_point(self, row, col):
        if 0 <= row < self.M and 0 <= col < self.N and self.board[row][col] == 0:
            self.board[row][col] = 1 if self.turn == 1 else 2
            return True
        return False


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


    #display game state
    def display_winner(self):
        player1 = None
        player2 = None
        if self.game_mode == "Human vs AI":
            player1 = self.human_player
            player2 = self.ai_player
        else:
            player1 = self.ai_player1
            player2 = self.ai_player2
        self.winner_label.configure(
            text=f"Winner:\n {player1 if self.turn == 1 else player2}",
            font=ctk.CTkFont("Arial", 22, "bold"),
            width=70,
            height=50,
            text_color="black",
            fg_color="#D4C9BE",
            corner_radius=10
        )
        self.winner_label.pack()

    def display_draw_message(self):
        self.draw_label.configure(
            text="Draw!",
            font=ctk.CTkFont("Arial", 22, "bold"),
            width=70,
            height=50,
            text_color="black",
            fg_color="#D4C9BE",
            corner_radius=10
        )
        self.draw_label.pack()

    #Temp Function
    def dummy(self):
        for row in range(self.M):
            for col in range(self.N):
                if self.board[row][col] == 0:
                    return row, col