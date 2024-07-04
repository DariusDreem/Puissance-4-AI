# MyCanva.py
import tkinter as tk

import GameType
from MyButton import MyButton

class MyCanvas(tk.Canvas):
    board = None
    fontSize = 16
    textTopBoard = None
    buttonRestart = None
    clickDeosntWork = False
    trainningIA = None

    # ========================== MENU ==========================

    def __init__(self, master):
        super().__init__(master)  # Appeler le constructeur de la classe parente
        self.master = master  # Stocker la référence à l'objet maître
        self.configure(bg='white')  # Configurer le fond de l'objet en blanc
        self.current_screen = None  # Initialiser l'écran actuel à None
        self.rows = 6  # Définir le nombre de lignes du tableau de jeu
        self.cols = 7  # Définir le nombre de colonnes du tableau de jeu
        self.cell_size = 100  # Définir la taille de chaque cellule
        self.board = self.master.game.board  # Obtenir le tableau de jeu depuis l'objet maître
        self.width = 380  # Définir la largeur de la fenêtre
        self.height = 350  # Définir la hauteur de la fenêtre
        self.config(width=self.width, height=self.height)  # Configurer les dimensions de la fenêtre

        self.canvas = self  # Référence au canvas actuel
        self.board = [[0] * self.cols for _ in range(self.rows)]  # Initialiser le tableau de jeu avec des zéros
        self.player = 1  # Définir le joueur actuel à 1
        self.show_menu()  # Afficher le menu principal
        print("MyCanvas init : ", self.master.game)  # Afficher l'état du jeu pour le débogage

    def show_menu(self):
        self.clear()  # Effacer le canvas
        self.current_screen = "menu"  # Définir l'écran actuel sur "menu"
        self.create_text(200, 40, text="Menu Screen", font=("Arial", 24), fill='black')  # Créer le texte du menu
        # Ajouter des boutons pour différentes options de jeu
        MyButton(self, 200, 150, "Joueur contre Joueur", self.start_game_pvp)
        MyButton(self, 200, 190, "Joueur contre Ordinateur", self.start_game_pve)
        MyButton(self, 200, 230, "Ordinateur contre Ordinateur", self.start_game_ia)
        MyButton(self, 200, 270, "Entraînement IA", self.Start_training_ia)
        MyButton(self, 200, 310, "Statistiques", self.Show_Stats)

    def start_game_pvp(self):
        self.clear()  # Effacer le canvas
        self.master.game.gameType = GameType.GameType.PVP  # Définir le type de jeu sur "Joueur contre Joueur"
        print("Game Type : ", self.master.game.gameType)  # Afficher le type de jeu pour le débogage
        self.setup_game()  # Configurer le jeu

    def start_game_pve(self):
        self.clear()  # Effacer le canvas
        self.master.game.gameType = GameType.GameType.PVC  # Définir le type de jeu sur "Joueur contre Ordinateur"
        print("Game Type : ", self.master.game.gameType)  # Afficher le type de jeu pour le débogage
        self.setup_game()  # Configurer le jeu
        self.master.game.SetPlayerPVC()  # Configurer les joueurs pour "Joueur contre Ordinateur"

    def start_game_ia(self):
        self.clear()  # Effacer le canvas
        self.master.game.gameType = GameType.GameType.CVC  # Définir le type de jeu sur "Ordinateur contre Ordinateur"
        print("Game Type : ", self.master.game.gameType)  # Afficher le type de jeu pour le débogage
        self.setup_game()  # Configurer le jeu
        self.master.game.SetPlayerCVC()  # Configurer les joueurs pour "Ordinateur contre Ordinateur"

    def Start_training_ia(self):
        self.clear()  # Effacer le canvas
        self.trainningIA = True  # Activer le mode entraînement IA
        self.master.game.gameType = GameType.GameType.CVC  # Définir le type de jeu sur "Ordinateur contre Ordinateur"
        print("Game Type : ", self.master.game.gameType)  # Afficher le type de jeu pour le débogage
        self.setup_game()  # Configurer le jeu
        self.master.game.SetPlayerCVC()  # Configurer les joueurs pour "Ordinateur contre Ordinateur"
        self.master.game.playTurn(-1)  # Commencer le tour de jeu pour l'IA

    def Show_Stats(self):
        # Analyser les premiers coups joués dans le jeu
        self.master.game.analyze_first_moves()
        print("Show Stats Here ^^")  # Afficher un message de débogage

    def back_to_menu(self):
        if self.current_screen == "game":  # Vérifier si l'écran actuel est le jeu
            self.show_menu()  # Afficher le menu
            self.master.unbind('m')  # Détacher la touche 'm'

    def clear(self):
        self.delete("all")  # Supprimer tous les éléments du canvas


    #======================= GAME =============================

    def setup_game(self):
        # Définir le nombre de lignes et de colonnes pour le jeu
        self.rows, self.cols = 6, 7

        # Définir la taille de chaque cellule
        self.cell_size = 100

        # Calculer la largeur et la hauteur totales de la fenêtre de jeu
        self.width = (self.cols * self.cell_size) + 10
        self.height = (self.rows + 1) * self.cell_size

        # Configurer les dimensions de la fenêtre
        self.config(width=self.width, height=self.height)

        # Dessiner le tableau de jeu initial
        self.draw_board()

        # Mettre à jour le dessin du tableau de jeu avec l'état actuel
        self.update_draw_board()

    def handle_click(self, event):
        # Vérifier si le jeu est terminé
        if self.master.game.IsFinished:
            return

        # Vérifier si les clics sont désactivés ou si le type de jeu est CVC (Computer vs. Computer)
        if self.clickDeosntWork or self.master.game.gameType is GameType.GameType.CVC:
            # Jouer un tour en fonction de la position du clic (colonne cliquée)
            self.master.game.playTurn(event.x // self.cell_size)
        else:
            # Si les clics ne sont pas autorisés, afficher un message et désactiver les clics
            print("Click doesn't work")
            self.clickDeosntWork = True


    def draw_board(self):
        for i in range(self.rows):  # Parcourir chaque ligne du tableau de jeu
            for j in range(self.cols):  # Parcourir chaque colonne du tableau de jeu
                # Calculer les coordonnées du coin supérieur gauche du rectangle
                x0 = j * self.cell_size + 5
                y0 = i * self.cell_size + 50

                # Calculer les coordonnées du coin inférieur droit du rectangle
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                # Créer un rectangle pour représenter la cellule
                self.create_rectangle(x0, y0, x1, y1, outline="black")

                # Vérifier si la cellule contient un jeton du joueur 1
                if self.board[i][j] == 1:
                    # Créer un cercle rouge pour le jeton du joueur 1
                    self.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red")
                # Vérifier si la cellule contient un jeton du joueur 2
                elif self.board[i][j] == 2:
                    # Créer un cercle jaune pour le jeton du joueur 2
                    self.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="yellow")

        # Associer un gestionnaire d'événements au canevas pour gérer les clics de souris pour les colones
        self.canvas.bind("<Button-1>", self.handle_click)

    def update_draw_board(self):
        # Supprimer tous les éléments du canvas
        self.delete("all")

        # Vérifier si le jeu est terminé
        if not self.master.game.IsFinished:
            # Le jeu n'est pas terminé, afficher le joueur actuel
            text = f"Joueur actuel {self.master.game.player_turn}"
        else:
            # Le jeu est terminé, afficher le joueur gagnant
            text = f"Joueur gagnant {self.master.game.player_turn}"

        # Créer le texte au centre du canvas
        self.create_text(self.winfo_reqwidth() // 2, self.fontSize, text=text,
                         font=("Helvetica", self.fontSize), fill="black")

        # Mettre à jour le tableau avec l'état actuel du jeu
        self.board = self.master.game.board
        # Dessiner le tableau de jeu
        self.draw_board()

        if not self.master.game.IsFinished:
            # Si le jeu n'est pas terminé, réappeler cette méthode après 100 ms
            self.after(100, self.update_draw_board)
        else:
            # Si le jeu est terminé, créer un bouton pour redémarrer le jeu
            self.buttonRestart = tk.Button(self.master, text="Restart Game", command=self.restart_game)
            self.buttonRestart.pack()

            print("self.trainningIA : ", self.trainningIA)
            if self.trainningIA:
                # Si l'IA est en entraînement, redémarrer le jeu sans intervention de l'utilisateur
                print("Training IA : New game")
                self.buttonRestart.pack_forget()
                self.master.game.ResetBoardGame()
                self.Start_training_ia()



    def restart_game(self):
        # Cacher le bouton de redémarrage du jeu
        self.buttonRestart.pack_forget()

        # Réinitialiser le tableau de jeu
        self.master.game.ResetBoardGame()

        # Afficher le menu principal
        self.show_menu()

        # Réinitialiser les dimensions de la fenêtre
        self.width = 230
        self.height = 500

        # Réinitialiser l'état du clic
        self.clickDeosntWork = False
