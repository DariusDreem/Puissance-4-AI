class Game:
    IsFinished = False
    
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.player_turn = 1

    def print_board(self):
        print("\n")
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print("\n")

    def is_valid_move(self, column):
        if column < 0 or column > 6:
            return False
        if (self.board[0][column] == 0):
            return True
        
        

    def make_move(self, column):
        for row in reversed(self.board):
            if row[column] == 0:
                row[column] = self.player_turn
                self.player_turn = 2 if self.player_turn == 1 else 1
                return

    def check_win(self):
        # Vérifier les lignes horizontales
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] != 0 and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return row[i]

        # Vérifier les colonnes verticales
        for col in range(len(self.board[0])):
            for row in range(len(self.board) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                    return self.board[row][col]

        # Vérifier les diagonales descendantes
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                    return self.board[row][col]

        # Vérifier les diagonales montantes
        for row in range(3, len(self.board)):
            for col in range(len(self.board[0]) - 3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]:
                    return self.board[row][col]

        return 0




    def play(self):
        self.IsFinished = False  # Initialiser la variable avec la casse correcte
        while not self.IsFinished:  # Utiliser la même casse dans la condition
            self.print_board()
            column = int(input("Enter column (0-6): "))
            if not self.is_valid_move(column):
                print("Invalid move. Try again.")
                continue
            self.make_move(column)
            winner = self.check_win()
            if winner:
                self.print_board()
                print(f"Player {winner} wins!")
                self.IsFinished = True  # Mettre à jour la variable avec la casse correcte
                break
            if all(cell != 0 for row in self.board for cell in row):
                self.print_board()
                print("It's a draw!")
                break
