import tkinter as tk
import GameType
from Connect4GUI import Connect4GUI
from Game import Game


class Menu:
    window = None

    def initWindowGame(self,root):
        gui = Connect4GUI(root)
        game = Game()
        game.setGUI(gui)
        return game

    def playpvp(self):
        print("Play PVP")

        self.window.destroy()  # Ferme la fenêtre du menu

        root = tk.Tk()
        game = self.initWindowGame(root)
        game.setGameType(GameType.GameType.PVP)
        game.play(root)
        self.window.quit()

    def playpve(self):
        print("Play")
        self.window.destroy()  # Ferme la fenêtre du menu

        root = tk.Tk()
        gui = Connect4GUI(root)
        game = Game()
        game.setGUI(gui)
        game.setGameType(GameType.GameType.PVC)
        game.play(root)

    def playeve(self):
        print("Play")
        self.window.destroy()  # Ferme la fenêtre du menu

        root = tk.Tk()
        gui = Connect4GUI(root)
        game = Game()
        game.setGUI(gui)
        game.setGameType(GameType.GameType.CVC)
        game.play(root)


    def __init__(self):
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
                                     font=("arial", 15),command=self.playpve)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(self.window, text="Ordinateur vs Ordinateur",
                                     font=("arial", 15), command=self.playeve)
        self.play_button.pack(pady=20)


        self.quit_button = tk.Button(self.window, text="Quitter",
                                     font=("arial", 15),
                                     command=self.window.quit)
        self.quit_button.pack(pady=20)

        self.window.mainloop()
