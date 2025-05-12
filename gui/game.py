import customtkinter as ctk
from gui.base import BaseScreen


class GameScreen(BaseScreen):
    def __init__(self, parent_frame, M, N, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.title_label = ctk.CTkLabel(self, text="Game Mode: " + game_mode, font=ctk.CTkFont("Arial", size=32, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)
        self.game_mode = game_mode
        self.M = M
        self.N = N
        self.turn = 1

        self.frame = ctk.CTkFrame(self, width=600, height=400, fg_color="#eaeaea")
        self.frame.place(relx=0.5, rely=0.53, anchor=ctk.CENTER)


        self.buttons = []

        for i in range(M):
            row = []
            for j in range(N):
                button = ctk.CTkButton(
                    self.frame,
                    text="",
                    width=600/M,
                    height=400/N,
                    font=ctk.CTkFont("Arial", size=16, weight="bold"),
                    fg_color="#363e47",
                    text_color="#ffffff",
                    corner_radius=2,
                    command=lambda x=i, y=j: self.get_input(x, y)
                )
                button.grid(row=i, column=j, padx=2, pady=2,sticky="nsew")
                row.append(button)
            self.buttons.append(row)

    def get_input(self, x, y):
        if self.game_mode == "AI vs AI":
            return
        if self.buttons[x][y].cget("text") == "":
            if self.turn == 1:
                self.buttons[x][y].configure(text= "W")
                self.turn = 2
            else:
                self.buttons[x][y].configure(text= "B")
                self.turn = 1
