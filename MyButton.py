# MyButton.py
import tkinter as tk

class MyButton:
    def __init__(self, canvas, x, y, text, command):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.command = command

        # Calculer la largeur du texte
        font = ("Arial", 16)
        text_width = self.canvas.create_text(0, 0, text=text, font=font, anchor="nw")
        bbox = self.canvas.bbox(text_width)
        self.canvas.delete(text_width)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        self.button_id = self.canvas.create_rectangle(x - width // 2 - 10, y - height // 2 - 5, x + width // 2 + 10, y + height // 2 + 5, outline="black", fill="lightgrey", tags="button")
        self.text_id = self.canvas.create_text(x, y, text=text, font=font, tags="button")

        self.canvas.tag_bind(self.button_id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.text_id, "<Button-1>", self.on_click)

    def on_click(self, event):
        self.command()
