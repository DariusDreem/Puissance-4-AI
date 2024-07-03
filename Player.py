class Player:
    def __init__(self):
        pass

    def Play(self, column, board, player_turn, columns_list, current_game):
        print("Player turn !!!")
        if column not in columns_list:
            print("Invalid move. Try again.")
            return
        return column