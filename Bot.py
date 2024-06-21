import Game
import random
class Bot:
    def __init__(self, player):
        self.player = player

    def play(self, board):
        Game.Game.playTurn(self, random.randint(0, 6))