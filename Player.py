class Player:
    def __init__(self):
        pass

    def Play(self, column, board, player_turn, columns_list, current_game):
        if column not in columns_list:
            return
        return column