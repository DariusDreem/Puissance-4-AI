import pandas as pd #type: ignore
import os
import random

class Bot:
    is_csv_file = False
    csv_file = None
    def __init__(self):
        self.csv_file = "./Data/Test.csv"
        self.games_data = None
        if os.path.exists(self.csv_file):
            self.games_data = pd.read_csv(self.csv_file)
            self.is_csv_file = True
        else:
            self.is_csv_file = False
            print(f"Le fichier {self.csv_file} n'existe pas. Le bot fonctionnera sans les données des parties précédentes.")

    def learn_from_games(self, current_game):
        if not self.is_csv_file or self.games_data is None:
            return None

        # Convertir current_game en une chaîne pour la comparaison
        current_game_str = ','.join([f"{move[0]},{move[1]}" for move in current_game])

        # Initialiser un dictionnaire pour stocker les scores moyens de chaque colonne
        column_scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        column_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # Parcourir toutes les parties dans le CSV
        for i in range(0, len(self.games_data.columns), 2):
            game_column = self.games_data.iloc[:, i]
            score_column = self.games_data.iloc[:, i+1]
            
            # Vérifier si la partie correspond à la partie actuelle
            game_moves = game_column.dropna().tolist()[1:]  # Ignorer la première ligne (Winner)
            game_str = ','.join(game_moves)
            
            if game_str.startswith(current_game_str):
                # Si la partie correspond, calculer le score pour chaque colonne
                for move, score in zip(game_moves[len(current_game):], score_column.dropna().tolist()[len(current_game):]):
                    col = int(move.split(',')[1])
                    column_scores[col] += float(score)
                    column_counts[col] += 1

        # Calculer la moyenne des scores pour chaque colonne
        for col in column_scores:
            if column_counts[col] > 0:
                column_scores[col] /= column_counts[col]

        # Trouver la colonne avec le meilleur score moyen
        best_col = max(column_scores, key=column_scores.get)
        
        return best_col
    
    def get_valid_col(self, columns_list):
        self.valid_col = columns_list
        
    def is_valid_move(self, col):
        return col in self.valid_col
    
    # @staticmethod
    def Play(self, column, board, player_turn, columns_list, current_game):
        print("Bot turn !!!")
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

        ## Si ni check_win ni check_block ne renvoient de coup, on regarde l'historique
        best_move = self.learn_from_games(current_game)

        # Évaluer chaque coup possible
        # best_score = float('-inf')
        # best_move = None
        # for col in range(7):
        #     if self.is_valid_move(col):
        #         temp_board = [row[:] for row in board]
        #         self.simulate_move(temp_board, col, player_turn)
        #         score = self.evaluate_board(temp_board, player_turn)
        #         if score > best_score:
        #             best_score = score
        #             best_move = col



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
    
    
    