import random

class Bot:
    move = 0

    def __init__(self):
        self.move = 0

    @staticmethod
    def Play():
        move = random.randint(0, 6)
        print("Bot played : ", move)
        return move