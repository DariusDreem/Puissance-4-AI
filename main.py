import game
import tkinter as tk
from Puissance4UI import Puissance4UI


def main():
    print("Welcome to Puissance-4!")

    root = tk.Tk()
    root.geometry("1200x700")  # Set an initial size for the window
    gameui = Puissance4UI(root)
    root.mainloop()

    game.Game().play()

    print("Game  ended.")




if __name__ == "__main__":
    main()
