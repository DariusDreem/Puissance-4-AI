class Player:
    def __init__(self):
        pass

    def Play(self, column, board, player_turn, columns_list):
        if column not in columns_list:
            print("Invalid move. Try again.")
            return