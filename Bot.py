import pandas as pd
import os
import random

class Bot:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.games_data = None
        if os.path.exists(csv_file):
            self.games_data = pd.read_csv(csv_file)
            self.learn_from_games()
        else:
            print(f"Le fichier {csv_file} n'existe pas. Le bot fonctionnera sans les données des parties précédentes.")

    def learn_from_games(self):
        # Analyse des parties précédentes pour ajuster la stratégie
        self.winning_moves = []
        for index, game in self.games_data.iteritems():
            if game[0] == 1:  # Si le joueur 1 a gagné
                self.winning_moves.append(game[1:].dropna().tolist())
    
    def get_valid_col(self, columns_list):
        self.valid_col = columns_list
        
    def is_valid_move(self, col):
        return col in self.valid_col
    
    # @staticmethod
    def Play(self, column, board, player_turn, columns_list):
        self.get_valid_col(columns_list)
        # Vérifier s'il y a un coup gagnant pour le bot
        for col in range(7):
            if self.is_valid_move(col):
                temp_board = [row[:] for row in board]
                self.simulate_move(temp_board, col, player_turn)
                if self.check_win(temp_board, player_turn):
                    return col

        # Vérifier s'il y a un coup gagnant pour l'adversaire à bloquer
        opponent = 1 if player_turn == 2 else 2
        for col in range(7):
            if self.is_valid_move(col):
                temp_board = [row[:] for row in board]
                self.simulate_move(temp_board, col, opponent)
                if self.check_win(temp_board, opponent):
                    return col

        # Évaluer chaque coup possible
        best_score = float('-inf')
        best_move = None
        for col in range(7):
            if self.is_valid_move(col):
                temp_board = [row[:] for row in board]
                self.simulate_move(temp_board, col, player_turn)
                score = self.evaluate_board(temp_board, player_turn)
                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move if best_move is not None else random.randint(0, 6)

    # @staticmethod
    def simulate_move(self, board, col, player):
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                board[row][col] = player
                break

    # @staticmethod
    def check_win(self, board, player):
        # Vérification horizontale
        for row in range(6):
            for col in range(4):
                if all(board[row][col+i] == player for i in range(4)):
                    return True

        # Vérification verticale
        for row in range(3):
            for col in range(7):
                if all(board[row+i][col] == player for i in range(4)):
                    return True

        # Vérification diagonale (descendante)
        for row in range(3):
            for col in range(4):
                if all(board[row+i][col+i] == player for i in range(4)):
                    return True

        # Vérification diagonale (montante)
        for row in range(3, 6):
            for col in range(4):
                if all(board[row-i][col+i] == player for i in range(4)):
                    return True

        return False

    # @staticmethod
    def evaluate_board(self, board, player):
        score = 0
        opponent = 1 if player == 2 else 2

        # Évaluer les lignes horizontales
        for row in range(6):
            for col in range(4):
                window = [board[row][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player)

        # Évaluer les colonnes verticales
        for row in range(3):
            for col in range(7):
                window = [board[row+i][col] for i in range(4)]
                score += Bot.evaluate_window(window, player)

        # Évaluer les diagonales descendantes
        for row in range(3):
            for col in range(4):
                window = [board[row+i][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player)

        # Évaluer les diagonales montantes
        for row in range(3, 6):
            for col in range(4):
                window = [board[row-i][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player)

        return score

    @staticmethod
    def evaluate_window(window, player):
        score = 0
        opponent = 1 if player == 2 else 2
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score