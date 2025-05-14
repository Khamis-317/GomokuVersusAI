import customtkinter as ctk
from gui.base import BaseScreen
from gui.game import GameScreen
from gui.instructions_page import Instructions
from exceptions.invalid_input_exception import InvalidInputException

class StartMenu(BaseScreen):
    def __init__(self, parent_frame):

        super().__init__(parent_frame, fg_color="#363e47", width=800, height=600)

        self.app_frame = parent_frame

        self.title_label = ctk.CTkLabel(self, text="Start Menu", font=ctk.CTkFont("Arial", size=42, weight="bold"))
        self.title_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

        self.error_label = ctk.CTkLabel(self, text_color="red", text="", font=ctk.CTkFont("Arial", size=12, weight="bold"))
        self.error_label.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

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

        self.button = ctk.CTkButton(self, height=35,width=50, text="How To Play", command=self.show_instructions)
        self.button.place(relx=0.6, rely=0.85, anchor=ctk.CENTER)

        self.button = ctk.CTkButton(self, height=35,text="Create Board", command=self.init_game)
        self.button.place(relx=0.4, rely=0.85, anchor=ctk.CENTER)

    def init_game(self):
        try:
            ROWS = int(self.height_entry.get())
            COLS = int(self.width_entry.get())
            if(ROWS < 5 or COLS < 5):
                raise InvalidInputException("Both board width and height must be greater than 5")
            game_mode = self.game_mode_options.get() 
            game_screen = GameScreen(self.app_frame, ROWS, COLS, game_mode)
            self.hide()
            game_screen.show()
        except InvalidInputException as e:
            self.error_label.configure(text=e)
        except:
            self.error_label.configure(text="Invalid input")


    def show_instructions(self):
        instructions_screen = Instructions(self.app_frame)
        self.hide()
        instructions_screen.show()
