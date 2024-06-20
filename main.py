import tkinter as tk
from Connect4GUI import Connect4GUI
from Game import Game


def main():
    print("Bienvenue dans Puissance-4!")

    root = tk.Tk()
    gui = Connect4GUI(root)
    game = Game()  # Passez l'instance de Connect4GUI à Game
    game.setGUI(gui)
    game.play(root)


if __name__ == "__main__":
    main()
