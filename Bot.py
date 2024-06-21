import random

class Bot:
    @staticmethod
    def Play(game):
        # Vérifier s'il y a un coup gagnant pour le bot
        for col in range(7):
            if game.is_valid_move(col):
                temp_board = [row[:] for row in game.board]
                Bot.simulate_move(temp_board, col, game.player_turn)
                if Bot.check_win(temp_board, game.player_turn):
                    return col

        # Vérifier s'il y a un coup gagnant pour l'adversaire à bloquer
        opponent = 1 if game.player_turn == 2 else 2
        for col in range(7):
            if game.is_valid_move(col):
                temp_board = [row[:] for row in game.board]
                Bot.simulate_move(temp_board, col, opponent)
                if Bot.check_win(temp_board, opponent):
                    return col

        # Évaluer chaque coup possible
        best_score = float('-inf')
        best_move = None
        for col in range(7):
            if game.is_valid_move(col):
                temp_board = [row[:] for row in game.board]
                Bot.simulate_move(temp_board, col, game.player_turn)
                score = Bot.evaluate_board(temp_board, game.player_turn)
                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move if best_move is not None else random.randint(0, 6)

    @staticmethod
    def simulate_move(board, col, player):
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                board[row][col] = player
                break

    @staticmethod
    def check_win(board, player):
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

    @staticmethod
    def evaluate_board(board, player):
        score = 0
        opponent = 1 if player == 2 else 2

        # Évaluer les lignes horizontales
        for row in range(6):
            for col in range(4):
                window = [board[row][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player, opponent)

        # Évaluer les colonnes verticales
        for row in range(3):
            for col in range(7):
                window = [board[row+i][col] for i in range(4)]
                score += Bot.evaluate_window(window, player, opponent)

        # Évaluer les diagonales descendantes
        for row in range(3):
            for col in range(4):
                window = [board[row+i][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player, opponent)

        # Évaluer les diagonales montantes
        for row in range(3, 6):
            for col in range(4):
                window = [board[row-i][col+i] for i in range(4)]
                score += Bot.evaluate_window(window, player, opponent)

        return score

    @staticmethod
    def evaluate_window(window, player, opponent):
        score = 0
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score