class GameEngine:
    def __init__(self, M, N, game_mode):
        for i in range(M):
            for j in range(N):
                self.board[i][j] = ""
        self.game_mode = game_mode
        self.turn = 1

    def start(self):
        pass
    def isValidMove(self) -> bool:
        pass
    def checkWin(self) -> int:
        pass
    def update(self, x, y):
        pass
    def display(self):
        pass