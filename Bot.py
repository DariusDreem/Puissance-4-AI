import pandas as pd #type: ignore
import numpy as np #type: ignore
import os
import random

class Bot:
    is_csv_file = False
    csv_file = None
    games_data = None
    valid_col = None
    
    def __init__(self, game_data=None):
        self.csv_file = "./Data/data.csv"
        self.game_data = game_data
            
    def learn_from_games(self, current_game):
        if not self.is_csv_file or self.games_data is None or self.games_data.empty or current_game is None:
            return None

        # Initialize a dictionary to store the average scores of each column
        column_scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        column_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # Iterate through all games in the CSV
        for i in range(0, len(self.games_data.columns) - 1, 2):
            if i + 1 >= len(self.games_data.columns):
                break  # Exit the loop if we've reached the end of columns

            game_column = self.games_data.iloc[:, i]
            score_column = self.games_data.iloc[:, i+1]
            
            # Check if the game matches the current game
            game_moves = game_column.dropna().tolist()[1:]  # Ignore the first row (Winner)
            
            if len(game_moves) >= len(current_game) and np.array_equal(current_game, game_moves[:len(current_game)]):
                # If the game matches, calculate the score for each column
                for move, score in zip(game_moves[len(current_game):], score_column.dropna().tolist()[len(current_game):]):
                    try:
                        col = int(move.split(',')[1])
                        if 0 <= col <= 6:  # Ensure the column is within valid range
                            column_scores[col] += float(score)
                            column_counts[col] += 1
                    except (ValueError, IndexError):
                        continue  # Skip invalid moves

        # Calculate the average score for each column
        for col in column_scores:
            if column_counts[col] > 0:
                column_scores[col] /= column_counts[col]

        # Find the column with the best average score
        best_col = max(column_scores, key=column_scores.get)
        print(f"Best column: {best_col} with score {column_scores[best_col]}")
        for col in column_scores:
            best_score = 0
            if best_score > column_scores[col] and col in self.valid_col:
                best_score = column_scores[col]
                best_move = col
            else: 
                continue
            best_col = best_move

        print(f"Best column: {best_col} with score {column_scores[best_col]}")    
            
        if best_col is None or best_score == 0 or best_score < 0:
            return None
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
        print("Bot Should Learn")
        best_move = self.learn_from_games(current_game)
        print("Best Move : ", best_move)
        if best_move is not None :
            return best_move
        else :
            self.get_valid_col(columns_list)
            return columns_list[random.randint(0, len(columns_list) - 1)] 

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
    
    
    