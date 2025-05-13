from abc import ABC, abstractmethod


class PlayMoveStrategy(ABC):
    @abstractmethod
    def makeMove(self, coordinateX, coordinateY):
        pass


class Player:
    def __init__(self, color, name, strategy: PlayMoveStrategy):
        self.name = name
        self.color = color
        self.strategy = strategy
        self.hasMoved = False

        if(color.lower() == "white"):
            self.colorBool = True
        else:
            self.colorBool = False


    def move(self, x, y):
        return self.strategy.makeMove(x, y)
        

class HumanPlayerStrategy(PlayMoveStrategy):
    def makeMove(self, x, y):
        x = int(input("Enter X coordinate: "))
        y = int(input("Enter Y coordinate: "))
        return x, y

    
class MinMaxAIPlayerStrategy(PlayMoveStrategy):
    def makeMove(self, x, y):
        pass

class AlphaBetaAIPlayerStrategy(PlayMoveStrategy):
    def makeMove(self, x, y):
        pass
