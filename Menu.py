import tkinter as tk


class Menu:

    def play(self):
        print("Play")
        # root = tk.Tk()
        # gui = Connect4GUI(root)
        # game = Game()  # Passez l'instance de Connect4GUI à Game
        # game.setGUI(gui)
        # game.play(root)

    def quit(self):
        print("Quit")
        # root.quit()

    def __init__(self):
        window = tk.Tk()
        window.title("Menu")
        window.geometry("400x400")
        window.resizable(False, False)

        self.label = tk.Label(window, text="Bienvenue dans Puissance-4!",
                              font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.play_button = tk.Button(window, text="Joueur vs Joueur",
                                     font=("arial", 15), command=self.play)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(window, text="Joueur vs Ordinateur",
                                     font=("arial", 15), command=self.play)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(window, text="Ordinateur vs Ordinateur",
                                     font=("arial", 15), command=self.play)
        self.play_button.pack(pady=20)


        self.quit_button = tk.Button(window, text="Quitter",
                                     font=("arial", 15),
                                     command=window.quit)
        self.quit_button.pack(pady=20)

        window.mainloop()
