import GameType
import Bot

class Game:
    gameType = GameType.GameType.PVP
    IsFinished = False
    _instance = None  # Variable de classe pour stocker l'unique instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, gui=None, gameType=None):
        if gui is not None:
            self.gui = gui
        if gameType is not None:
            self.GameType = GameType.GameType(gameType)

        if not hasattr(self,
                       'initialized'):  # Vérifiez si l'instance a déjà été initialisée
            self.board = [[0 for _ in range(7)] for _ in range(6)]
            self.player_turn = 1
            self.initialized = True  # Marquez l'instance comme initialisée
            self.gameType = GameType.GameType.PVP

    def setGUI(self, gui):
        self.gui = gui  # Instance de Connect4GUI

    def setGameType(self, gameType):
        self.gameType = gameType  # Instance de Connect4GUI

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
        i = 0
        for row in reversed(self.board):
            if row[column] == 0:
                print("ligne : ", i, " colonne : ", column, " joueur : ", self.player_turn)

                row[column] = self.player_turn

                self.gui.place_token(5 - i, column,
                                     self.player_turn)
                self.player_turn = 2 if self.player_turn == 1 else 1
                break
            i += 1

    # for row in reversed(self.board):
    #         if row[column] == 0:
    #             row[column] = self.player_turn
    #             self.gui.update_display(
    #                 self.board)  # Appel à la méthode de Connect4GUI
    #             self.player_turn = 2 if self.player_turn == 1 else 1
    #             return

    def check_win(self):
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
            self.IsFinished = True
            self.gui.display_winner(self.board[row][col])
            self.IsFinished = True
            self.DisplayWinner(winner)
            
    def display_winner(self, player):
        player_color = "rouge" if self.player == 1 else "jaune"
        self.current_player_label.config(text=f"Le gagant est {player_color}")
            
    def check_draw(self):
        if all(cell != 0 for row in self.board for cell in row):
            print("It's a draw!")
            self.IsFinished = True
    
    def playTurn(self, column):
        print(self.gameType)
        print(GameType.GameType.PVP)
        if GameType.GameType.PVP is self.gameType:
            print("caca")
            self.PlayerPlay(column)
        elif GameType.GameType.PVC == self.gameType:

            if (self.player_turn == 1):
                self.PlayerPlay(column)
            else:
                self.BotPlay()
        elif GameType.GameType.CVC == self.gameType:
            self.BotPlay()
        self.check_win()
        self.check_draw()
        
    def BotPlay(self):
        move = Bot.Bot.Play()
        self.make_move(move)
       
        #self.print_board()
    
    
    def PlayerPlay(self, column):
        if not self.is_valid_move(column):
            print("Invalid move. Try again.")
            return
        self.make_move(column)
        #self.print_board()

        

    def play(self, root):
        self.IsFinished = False  # Initialiser la variable avec la casse correcte
        root.mainloop()  # Now the game will run on GUI and He update only the GUI
