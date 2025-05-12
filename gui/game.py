import customtkinter as ctk
from gui.base import BaseScreen


class GameScreen(BaseScreen):
    def __init__(self, parent_frame, M, N, game_mode):
        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.title_label = ctk.CTkLabel(self, text="THE GAME IS ON!", font=ctk.CTkFont("Arial", size=42, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)
