import tkinter as tk


# Définir une classe personnalisée qui hérite de tk.Label
class MyLabel(tk.Label):
    def __init__(self, parent, text, bg="grey", fg="black",
                 font=("Helvetica", 12), **kwargs):
        super().__init__(parent, text=text, bg=bg, fg=fg, font=font, **kwargs)
        self.pack()

    def change_text(self, new_text):
        self.config(text=new_text)
