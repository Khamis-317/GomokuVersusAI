import customtkinter as ctk
from gui.start_menu import StartMenu
from gui.game import GameScreen

# Main window class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Gomoku")

if __name__ == "__main__":
    # setup
    ctk.set_appearance_mode("dark")    # "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    app = App()
    app.configure(fg_color = ("#363e47"))

    game_screen = GameScreen(app)
    start_menu = StartMenu(app, game_screen)

    start_menu.show()
    app.mainloop()