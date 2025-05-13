import customtkinter as ctk
import tkinter as tk
from gui.base import BaseScreen

class Instructions(BaseScreen):
    def __init__(self, parent_frame):

        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)
        self.app_frame = parent_frame

        ctk.CTkLabel(
            self,
            text=f"Gomuko Rules",
            font=ctk.CTkFont("Arial", 28, "bold"),
            text_color="white"
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text=(
                "Welcome to Gomoku!\n\n"
                "Start by entering the board dimensions on the start menu.\n\n"
                "Then choose one of the game modes:\n\n"
                " - Human vs AI (Minimax)\n\n"
                " - AI vs AI (Minimax vs Alpha-Beta Pruning)\n\n"
                "The objective is to be the first to align 5 checkers in a row:\n\n"
                " -Horizontally, Diagonally, Vertically\n"
                ""
            ),
            font=ctk.CTkFont("Arial", 22),
            text_color="white",
            justify="center",  # This helps center lines
            width=700,
            anchor="center"
        ).pack(pady=20)

        self.back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.back_to_menu,
            font=ctk.CTkFont("Arial", 18),
            text_color="white"
        )
        self.back_button.place(relx=0.11, rely=0.1, anchor=ctk.CENTER)

    def back_to_menu(self):
        from gui.start_menu import StartMenu
        self.destroy()
        start_menu = StartMenu(self.app_frame)
        start_menu.show()