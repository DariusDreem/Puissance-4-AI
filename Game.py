import GameType
import Bot as Bot
import Player as Player


class Game:
    gameType = GameType.GameType.PVP
    IsFinished = False
    _instance = None  # Variable de classe pour stocker l'unique instance
    player1 = Player.Player()
    player2 = Player.Player()
    player_turn = 1
    actuel_player = 1 if player_turn == 1 else 2
    board = [[0 for _ in range(7)] for _ in range(6)]

    def __new__(cls, args=None):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, gameType=None):
        if gameType is not None:
            print("Set Game Type : ", gameType)
            self.GameType = GameType.GameType(gameType)

        if not hasattr(self,
                       'initialized'):  # Vérifiez si l'instance a déjà été initialisée
            self.player_turn = 1
            self.initialized = True  # Marquez l'instance comme initialisée
            self.gameType = GameType.GameType.PVP

    def setGameType(self, gameType):
        self.gameType = gameType  # Instance de Connect4GUI
        

    def print_board(self):
        print("\n")
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print("\n")

    def is_valid_move(self):
        valid_moves = []
        for column in range(7):
            if self.board[0][column] == 0:
                valid_moves.append(column)
        return valid_moves

    def finishLoadGui(self):
        print("Finish Load Gui")
        print("Game Type : ", self.gameType)
        print("Player turn : ", GameType.GameType.CVC)
        if GameType.GameType.CVC == self.gameType:
            # print(gui)
            self.playTurn(-1, False)

    def make_move(self, column):
        i = 0
        if self.IsFinished:
            return

        print("Column : ", column)
        print("board : ", self.board)
        for row in reversed(self.board):
            print("Row : ", row)
            print("Column : ", row[column])
            if row[column] == 0:
                print("ligne : ", i, " colonne : ", column, " joueur : ",
                      self.player_turn)

                row[column] = self.player_turn
                # Place a Token in the board

                self.player_turn = 2 if self.player_turn == 1 else 1
                actuel_player = self.player1 if self.player_turn == 1 else self.player2
                break
            i += 1
        print("Player turn : ", self.gameType)
        if GameType.GameType.CVC == self.gameType:
            print("Bot turn !!!")
            #Loop for the bot to play

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
            self.IsFinished = True

    def check_draw(self):
        if all(cell != 0 for row in self.board for cell in row):
            print("It's a draw!")
            self.IsFinished = True

    def SetPlayerPVC(self):
        self.player1 = Player.Player()
        self.player2 = Bot.Bot()
    
    def SetPlayerCVC(self):
        self.player1 = Bot.Bot()
        self.player2 = Bot.Bot()
        print("Set Player CVC")



    def playTurn(self, column=0, playerClick=True):
        print(self.gameType)
        if self.gameType == GameType.GameType.CVC:
            while not self.IsFinished:
                print("while entered")
                column = self.player1.Play(column, self.board, self.player_turn,self.is_valid_move()) if self.player_turn == 1 else self.player2.Play(column, self.board, self.player_turn, self.is_valid_move())
                self.make_move(column)
                self.check_win()
                self.check_draw()
        # elif GameType.GameType.PVC == self.gameType:

        #     if (self.player_turn == 1):
        #         self.PlayerPlay(column)
        #     else:
        #         self.BotPlay()
        # elif GameType.GameType.CVC == self.gameType:
        #     self.BotPlay()
        column = self.player1.Play(column, self.board, self.player_turn,
                                   self.is_valid_move()) if self.player_turn == 1 else self.player2.Play(
            column, self.board, self.player_turn, self.is_valid_move())
        self.make_move(column)
        self.check_win()
        self.check_draw()

    def BotPlay(self):
        bot = Bot.Bot()
        column = bot.Play(self.board, self.player_turn, self.is_valid_move())
        self.make_move(column)

    def PlayerPlay(self, column):
        if column not in self.is_valid_move():
            print("Invalid move. Try again.")
            return
        self.make_move(column)

    def play(self, root):
        self.IsFinished = False  # Initialiser la variable avec la casse correcte
        root.mainloop()  # Now the game will run on GUI and He update only the GUI

