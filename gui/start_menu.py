import customtkinter as ctk
from gui.base import BaseScreen

class StartMenu(BaseScreen):
    def __init__(self, parent_frame, next_frame=None):

        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)

        self.title_label = ctk.CTkLabel(self, text="Start Menu", font=ctk.CTkFont("Arial", size=42, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

        self.width_label = ctk.CTkLabel(self, text="Board width", font=ctk.CTkFont("Arial", size=18, weight="bold"))
        self.width_label.place(relx=0.25, rely=0.35, anchor=ctk.W)
        self.width_entry = ctk.CTkEntry(self, width=220, height=25, placeholder_text="Enter board width..")
        self.width_entry.place(relx=0.45, rely=0.35, anchor=ctk.W)

        self.height_label = ctk.CTkLabel(self, text="Board height", font=ctk.CTkFont("Arial", size=18, weight="bold"))
        self.height_label.place(relx=0.25, rely=0.5, anchor=ctk.W)
        self.height_entry = ctk.CTkEntry(self, width=220, height=25, placeholder_text="Enter board height..")
        self.height_entry.place(relx=0.45, rely=0.5, anchor=ctk.W)

        self.game_mode_label = ctk.CTkLabel(self, text="Choose the game mode", font=ctk.CTkFont("Arial", size=18, weight="bold"))
        self.game_mode_label.place(relx=0.25, rely=0.65, anchor=ctk.W)

        self.game_mode_options = ctk.CTkOptionMenu(self, width=135, height=20, values=["Human vs AI", "AI vs AI"])
        self.game_mode_options.place(relx=0.55, rely=0.65, anchor=ctk.W)

        self.button = ctk.CTkButton(self, height=35, text="Start Game", command= lambda:self.switch_screen(self, next_frame))
        self.button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

    def switch_screen(self, current_screen, new_screen):
        # TODO: input validation
        super().switch_screen(current_screen, new_screen)
        