from strategies.movement import Movement

class Dummy(Movement):
    def __init__(self, M, N):
        self.M = M
        self.N = N

    def make_move(self, board) -> tuple:
           for row in range(self.M):
            for col in range(self.N):
                if board[row][col] == 0:
                    return row, col
                
    def __str__(self):
        return "Dummy AI"