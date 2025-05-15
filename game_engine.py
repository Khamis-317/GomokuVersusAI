from time import sleep
from strategies.alpha_beta import Alpha_Beta
class GameEngine:
    def __init__(self, ROWS, COLS, players):
        self.M = ROWS  # number of rows
        self.N = COLS  # number of cols
        # board initialization
        self.board = []
        for i in range(ROWS):
            row = [0] * COLS
            self.board.append(row)
        self.round_count = 0
        self.running = False
        self.player1 = players[0]
        self.player2 = players[1]
        self.turn = 1
        self.end_result = None

    def start(self):
        self.running = True

    # mark the game board if the move is valid
    def mark_valid_move(self, row, col):
        if 0 <= row < self.M and 0 <= col < self.N and self.board[row][col] == 0:
            self.board[row][col] = 1 if self.turn == 1 else 2
            return True
        return False

    # return the start and end of the winning sequence an None if there's no winner
    def check_win(self, row, col):
        WINNING_SEQ = 5
        dx = [1,0,1,1,0,-1,-1,-1]
        dy = [0,1,1,-1,-1,-1,0,1]
        # check 8 directions
        #(-1,-1) | ( 0,-1) | (+1,-1)
        #(-1, 0) | (row, col) | (+1, 0)
        #(-1, +1) | ( 0, +1) | (-1, +1)
        r = 0
        c = 0
        # check for a wining sequence at each direction around the last played cell
        for dr, dc in zip(dx,dy):
            # skipping the current cell and starting the count at 1
            count = 1
            for i in range(1, 5):
                r,c = row + dr * i , col + dc * i
                if 0 <= r < self.M and 0 <= c < self.N and self.board[r][c] == self.board[row][col]:
                    count += 1
                else:
                    break
            if count == WINNING_SEQ:
                start = (col, row)
                end = (c, r)
                # return the start and end points of the winning sequence
                return (start, end)
        return None

    def is_board_full(self):
        return self.round_count == self.M*self.N
    
    def game_loop(self, draw_point):
        while self.running:
            move = None
            if self.turn == 1:
                move = self.player1.make_move(self.board)
            else:
                move = self.player2.make_move(self.board)
            if move is not None:
                row, col = move
                if self.mark_valid_move(row, col):
                    color = "white" if self.turn == 1 else "red"
                    self.round_count += 1
                    draw_point(row, col, color)

                    win = self.check_win(row, col)
                    if win:
                        self.running = False
                        # winner's turn, x1, y1, x2, y2 are returned
                        return self.turn, win[0], win[1]

                    if self.is_board_full():
                        self.running = False
                        return None

                    self.turn = 1 if self.turn == 2 else 2
                    sleep(0.1)
    
    def reset(self):
        self.turn = 1
        self.round_count = 0
        for i in range(self.M):
            for j in range(self.N):
                self.board[i][j] = 0