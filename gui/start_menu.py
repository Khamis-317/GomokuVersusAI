import customtkinter as ctk

class StartMenu:
    def __init__(self, parent_frame, next_frame):

        self.menu = ctk.CTkFrame(parent_frame, fg_color="#363e47", width=600, height=500)

        self.title_label = ctk.CTkLabel(self.menu, text="Start Menu", font=ctk.CTkFont("Arial", size=42, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

        self.width_label = ctk.CTkLabel(self.menu, text="Board width", font=ctk.CTkFont("Arial", size=16, weight="bold"))
        self.width_label.place(relx=0.2, rely=0.35, anchor=ctk.W)
        self.width_entry = ctk.CTkEntry(self.menu, width=220, placeholder_text="Enter board width..")
        self.width_entry.place(relx=0.4, rely=0.35, anchor=ctk.W)

        self.height_label = ctk.CTkLabel(self.menu, text="Board height", font=ctk.CTkFont("Arial", size=16, weight="bold"))
        self.height_label.place(relx=0.2, rely=0.5, anchor=ctk.W)
        self.height_entry = ctk.CTkEntry(self.menu, width=220, placeholder_text="Enter board height..")
        self.height_entry.place(relx=0.4, rely=0.5, anchor=ctk.W)

        self.game_mode_label = ctk.CTkLabel(self.menu, text="Choose the game mode", font=ctk.CTkFont("Arial", size=16, weight="bold"))
        self.game_mode_label.place(relx=0.2, rely=0.65, anchor=ctk.W)

        self.game_mode_options = ctk.CTkOptionMenu(self.menu, width=120, height=20, values=["Human vs AI", "AI vs AI"])
        self.game_mode_options.place(relx=0.55, rely=0.65, anchor=ctk.W)

        self.button = ctk.CTkButton(self.menu, height=35, text="Start Game", command=None)
        self.button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

    def show(self):
        self.menu.pack(pady=(50, 0))

    def hide(self):
        self.menu.pack_forget()