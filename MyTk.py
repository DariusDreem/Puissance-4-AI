# mytk.py
import tkinter as tk

from Game import Game
from MyCanva import MyCanvas


class MyTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.game = Game(self)
        self.canvas = MyCanvas(self)
        self.canvas.pack(fill="both", expand=True)


