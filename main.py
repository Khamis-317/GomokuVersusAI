import customtkinter as ctk

app = ctk.CTk()  # create the Tk window like you normally do
app.geometry("800x600")
app.title("CustomTkinter Test")

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = ctk.CTkButton(master=app, corner_radius=10, command=button_function)
button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

app.mainloop()