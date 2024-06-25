import tkinter as tk
import GameType
from Connect4GUI import Connect4GUI
from Game import Game


class Menu:
    window = None
    menun = None

    def initWindowGame(self, root):
        gui = Connect4GUI(root)
        game = Game()
        game.setGUI(gui)
        game.setMenu(self)
        return game

    def playpvp(self):
        print("Play PVP")

        self.hiddenFrame()

        root = tk.Tk()
        game = self.initWindowGame(root)
        game.setGameType(GameType.GameType.PVP)

        game.play(root)

    def playpve(self):
        print("Play PVE")


        root = tk.Tk()
        game = self.initWindowGame(root)
        game.setGameType(GameType.GameType.PVC)

        game.play(root)
        self.window.quit()

    def playeve(self):
        print("Play EVE")
        root = tk.Tk()
        gui = Connect4GUI(root)
        game = Game(gui, GameType.GameType.PVC, self)
        game.setGUI(gui)
        game.play(root)

    def __init__(self):
        self.quit_button = None
        self.label = None
        print("Menu")
        self.printMenu()

    def printMenu(self):
        self.window = tk.Tk()
        self.window.title("Menu")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        self.label = tk.Label(self.window, text="Bienvenue dans Puissance-4!",
                              font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.play_button = tk.Button(self.window, text="Joueur vs Joueur",
                                     font=("arial", 15), command=self.playpvp)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(self.window, text="Joueur vs Ordinateur",
                                     font=("arial", 15), command=self.playpve)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(self.window,
                                     text="Ordinateur vs Ordinateur",
                                     font=("arial", 15), command=self.playeve)
        self.play_button.pack(pady=20)

        self.quit_button = tk.Button(self.window, text="Quitter",
                                     font=("arial", 15),
                                     command=self.window.quit)
        self.quit_button.pack(pady=20)

        self.window.mainloop()

    def hiddenFrame(self):
        self.window.withdraw()

    def openFrame(self):
        self.window.deiconify()
        self.window.mainloop()