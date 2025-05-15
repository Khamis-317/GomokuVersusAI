import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen
from game_engine import GameEngine
from strategies.human import Human
from strategies.dummy import Dummy
import threading
from strategies.alpha_beta import Alpha_Beta
class GameScreen(BaseScreen):
    def __init__(self, parent_frame, ROWS, COLS, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.parent_frame = parent_frame
        self.M = ROWS  # number of rows
        self.N = COLS  # number of cols
        self.cell_size = 40
        self.margin = 20
        self.game_mode = game_mode

        # players
        if self.game_mode == "Human vs AI":
            self.player1 = Human(ROWS, COLS, self.click)  # human
            self.player2 = Alpha_Beta(ROWS, COLS, 4)  # replace with minimax instance
        else:
            self.player1 = Alpha_Beta(ROWS, COLS, 4)   # replace with alpha-beta instance
            self.player2 = Dummy(ROWS, COLS)   # replace with minimax instance

        self.game_engine = GameEngine(ROWS, COLS, (self.player1, self.player2))

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


    def click(self, event):
        if self.game_mode == "Human vs AI" and self.game_engine.turn == 1:
            col = round((event.x - self.margin) / self.cell_size)
            row = round((event.y - self.margin) / self.cell_size)
            # set the position of the player move
            self.player1.set_click_pos(row, col)
            # set click_event flag to wait for a click at the gameloop thread
            self.player1.click_event.set()

    # running the game loop in another thread to prevent it 
    # from blocking the GUI as it runs on the main thread
    def run_game_loop(self):
        end_result = self.game_engine.game_loop(self.draw_point)

        if end_result:
            winner_turn, start, end = end_result
            self.draw_winning_sequence(start, end)
            self.display_winner(winner_turn)
        else:
            self.display_draw_message()


    def start_game(self):
        self.game_started = True
        self.start_button.configure(state="disabled")
        self.reset_button.configure(state="enabled")
        self.back_button.configure(state="disabled")

        self.game_engine.start()
        # starting a thread to run the gameloop separated from the GUI
        game_thread = threading.Thread(target=self.run_game_loop)
        game_thread.start()


    def reset_game(self):
        self.start_button.configure(state="normal")
        self.game_engine.reset()
        self.canvas.delete("all")
        self.draw_grid()
        self.winner_label.pack_forget()
        self.draw_label.pack_forget()
        self.back_button.configure(state="normal")
        self.reset_button.configure(state="disabled")

    def back_to_menu(self):
        from gui.start_menu import StartMenu
        self.destroy()
        start_menu = StartMenu(self.parent_frame)
        start_menu.show()

    # Canvas Drawing
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

    def draw_winning_sequence(self, start, end):
        x1 = start[0] * self.cell_size + self.margin
        y1 = start[1] * self.cell_size + self.margin
        x2 = end[0] * self.cell_size + self.margin
        y2 = end[1] * self.cell_size + self.margin
        self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=5)


    #display game state
    def display_winner(self, winner_turn):
        self.winner_label.configure(
            text=f"Winner:\n {self.player1 if winner_turn == 1 else self.player2}",
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