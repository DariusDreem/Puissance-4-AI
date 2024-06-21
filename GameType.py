from enum import Enum

class GameType(Enum):
    """
    Enum class to represent the type of game.
    """
    PVP = 1
    PVC = 2
    CVC = 3
    
    def __str__(self):
        return self.name