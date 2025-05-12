import customtkinter as ctk


class BaseScreen(ctk.CTkFrame):
    def __init__(self, parent_frame, fg_color, width, height):
        super().__init__(parent_frame, fg_color=fg_color, width=width, height=height)

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()
    
  