class Player:
    __init__ = None

    def Play(self,column ,board, player_turn, columns_list) :
         if column not in columns_list:
            print("Invalid move. Try again.")
            return
        