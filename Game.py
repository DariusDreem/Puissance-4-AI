import GameType
import Bot as Bot
import Player as Player
import os
import numpy as np  #type: ignore
import matplotlib.pyplot as plt  #type: ignore
import pandas as pd  #type: ignore
from collections import Counter
import random

from Stats import Puissance4CSV


class Game:
    gameType = GameType.GameType.PVP
    IsFinished = False
    _instance = None  # Variable de classe pour stocker l'unique instance
    player1 = Player.Player()
    player2 = Player.Player()
    player_turn = 1
    actuel_player = 1 if player_turn == 1 else 2
    board = [[0 for _ in range(7)] for _ in range(6)]
    player_data = None
    csv_file = None
    games_data = None   # Variable de classe pour stocker les données des parties

    def __new__(cls, args=None):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, myTk=None):
        self.master = myTk
        self.csv_file = "./Data/data.csv"
        self.player_data = Puissance4CSV()
        if os.path.exists(self.csv_file):
            print("File exist")
            if os.path.getsize(self.csv_file) > 0:
                
                self.games_data = pd.read_csv(self.csv_file, sep=';', low_memory=False,index_col= 0)
                
            
            print(self.games_data)
            print("File loaded")
        if not hasattr(self,
                       'initialized'):  # Vérifiez si l'instance a déjà été initialisée
            self.player_turn = 1
            self.initialized = True  # Marquez l'instance comme initialisée
            self.gameType = GameType.GameType.PVP

    def setGameType(self, gameType):
        self.gameType = gameType  # Instance de Connect4GUI

    def ResetBoardGame(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.IsFinished = False
        self.player_turn = 1

    def is_valid_move(self):
        valid_moves = []
        for column in range(7):
            if self.board[0][column] == 0:
                valid_moves.append(column)
        return valid_moves

    def finishLoadGui(self):
        if GameType.GameType.CVC == self.gameType:
            self.playTurn(-1, False)

    def make_move(self, column):
        i = 0
        if self.IsFinished:
            return

        for row in reversed(self.board):
            if row[column] == 0:
                row[column] = self.player_turn

                self.player_turn = 2 if self.player_turn == 1 else 1
                actuel_player = self.player1 if self.player_turn == 1 else self.player2
                self.player_data.AjouterLigne([i, column])
                break
            i += 1

    def check_win(self):
        winner = 0

        # Vérifier les lignes horizontales
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] != 0 and row[i] == row[i + 1] == row[i + 2] == row[
                    i + 3]:
                    winner = row[i]

        # Vérifier les colonnes verticales
        for col in range(len(self.board[0])):
            for row in range(len(self.board) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == \
                        self.board[row + 1][col] == self.board[row + 2][col] == \
                        self.board[row + 3][col]:
                    winner = self.board[row][col]

        # Vérifier les diagonales descendantes
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == \
                        self.board[row + 1][col + 1] == self.board[row + 2][
                    col + 2] == self.board[row + 3][col + 3]:
                    winner = self.board[row][col]

        # Vérifier les diagonales montantes
        for row in range(3, len(self.board)):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == \
                        self.board[row - 1][col + 1] == self.board[row - 2][
                    col + 2] == self.board[row - 3][col + 3]:
                    winner = self.board[row][col]

        if winner != 0:
            self.player_data.Sauvegarder(winner)
            self.IsFinished = True

    def check_draw(self):
        if all(cell != 0 for row in self.board for cell in row):
            self.IsFinished = True

    def SetPlayerPVC(self):
        randomint = random.randint(0, 1)
        if randomint == 0:
            self.player1 = Player.Player()
            self.player2 = Bot.Bot(self.games_data)
        else:
            self.player1 = Bot.Bot(self.games_data)
            self.player2 = Player.Player()

    def SetPlayerCVC(self):
        self.player1 = Bot.Bot(self.games_data)
        self.player2 = Bot.Bot(self.games_data)

    def playTurn(self, column=0, playerClick=True):
        if self.gameType == GameType.GameType.PVP:
            self.player1 = Player.Player()
            self.player2 = Player.Player()
        if (self.gameType == GameType.GameType.PVC and type(
                self.player1) is not Bot.Bot):
            if (type(self.player2) is not Bot.Bot):
                self.SetPlayerPVC()

        if (self.gameType == GameType.GameType.CVC and type(
                self.player1) is not Bot.Bot) or (
                self.gameType == GameType.GameType.CVC and type(
                self.player2) is not Bot.Bot):
            self.SetPlayerCVC()

        if self.gameType == GameType.GameType.CVC:    
            while not self.IsFinished:

                column = self.player1.Play(column, self.board, self.player_turn,
                                           self.is_valid_move(),
                                           self.player_data.arrayTurn) if self.player_turn == 1 else self.player2.Play(
                    column, self.board, self.player_turn, self.is_valid_move(),
                    self.player_data.arrayTurn)
                self.make_move(column)
                self.check_win()
                self.check_draw()
                # self.master.after(100, self.master.update())

              
        column = self.player1.Play(column, self.board, self.player_turn,
                                   self.is_valid_move(),
                                   self.player_data.arrayTurn) if self.player_turn == 1 else self.player2.Play(
            column, self.board, self.player_turn, self.is_valid_move(),
            self.player_data.arrayTurn)
        self.make_move(column)
        self.check_win()
        self.check_draw()

    def PlayerPlay(self, column):
        if column not in self.is_valid_move():
          
            return
        self.make_move(column)

    def play(self, root):
        self.IsFinished = False  # Initialiser la variable avec la casse correcte
        root.mainloop()  # Now the game will run on GUI and He update only the GUI

    # def analyze_first_moves():
    #     games = [Game() for _ in range(1000)]
    #     first_moves = [game.first_move for game in games]
    #
    #     # Compter la fréquence de chaque premier coup
    #     move_counts = Counter(first_moves)
    #
    #     # Trier les coups par fréquence décroissante
    #     sorted_moves = sorted(move_counts.items(), key=lambda x: x[1], reverse=True)
    #
    #     # Séparer les coups et les comptages pour le graphique
    #     moves, counts = zip(*sorted_moves)
    #
    #     # Créer le graphique
    #     plt.figure(figsize=(12, 6))
    #     plt.bar(moves, counts)
    #
    #     # Personnaliser le graphique
    #     plt.title("Fréquence des premiers coups")
    #     plt.xlabel("Premier coup")
    #     plt.ylabel("Nombre de parties")
    #     plt.xticks(rotation=45, ha='right')
    #
    #     # Ajuster la mise en page
    #     plt.tight_layout()
    #
    #     # Afficher le graphique
    #     plt.show()
    #
    #
    def analyze_first_moves(self):

        if self.games_data is None or self.games_data.empty:
            return None

        # Initialiser un dictionnaire pour stocker le nombre de premiers coups dans chaque colonne
        first_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # Parcourir toutes les parties dans le CSV
        for i in range(0, len(self.games_data.columns) - 1, 2):
            if i + 1 >= len(self.games_data.columns):
                break  # Sortir de la boucle si on a atteint la fin des colonnes

            game_column = self.games_data.iloc[2, i]
            # Obtenir le premier coup (en ignorant la première ligne qui contient "Winner")
            first_move = game_column[4]
            try:
                col = int(first_move)
                if 0 <= col <= 6:  # S'assurer que la colonne est dans la plage valide
                    first_moves[col] += 1
            except (ValueError, IndexError):
                continue  # Ignorer les coups invalides
        # Calculer le pourcentage de premiers coups pour chaque colonne
        total_games = sum(first_moves.values())
        first_move_percentages = {col: (count / total_games) * 100 for
                                  col, count in first_moves.items()}
        # Créer un graphique à barres
        plt.figure(figsize=(10, 6))
        plt.bar(first_move_percentages.keys(), first_move_percentages.values())
        plt.title("Répartition des premiers coups")
        plt.xlabel("Colonne")
        plt.ylabel("Pourcentage de premiers coups")
        plt.xticks(range(7))
        plt.xlim(-0.5, 6.5)
        plt.ylim(0, 100)

        # Ajouter les pourcentages au-dessus de chaque barre
        for col, percentage in first_move_percentages.items():
            plt.text(col, percentage, f'{percentage:.1f}%', ha='center',
                     va='bottom')

        plt.show()

        # Trouver la colonne la plus jouée en premier
        most_played_column = max(first_moves, key=first_moves.get)
        print(f"Colonne la plus jouée en premier : {most_played_column}")

        return most_played_column