from strategies.movement import Movement

class Human(Movement):
    def __init__(self, M, N, action):
        self.M = M
        self.N = N
        self.action = action

    def make_move(self, board) -> tuple:
        row, col = self.action()
        return row, col
    
    def __str__(self):
        return "Human"