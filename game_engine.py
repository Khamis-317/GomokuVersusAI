from time import sleep

class GameEngine:
    def __init__(self, ROWS, COLS, game_mode):
        self.M = ROWS  # number of rows
        self.N = COLS  # number of cols
        self.board = []
        self.round_count = 0
        self.running = False
        self.turn = 1
        if game_mode == "Human vs AI":
            self.player1 = None  # human
            self.player2 = None  # replace with minimax instance
        else:
            self.player1 = None  # replace with alpha-beta instance
            self.player2 = None  # replace with minimax instance
        # self.game_mode = game_mode

    def start_game(self):
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
                x1 = col * self.cell_size + self.margin
                y1 = row * self.cell_size + self.margin
                x2 = c * self.cell_size + self.margin
                y2 = r * self.cell_size + self.margin
                # return the start and end of the winning sequence
                return ((x1, y1), (x2, y2))
        return None

    def is_board_full(self):
        return self.round_count == self.M*self.N
    
    def update(self):
        while self.running:
            move = None
            if(self.turn == 1):
                move = self.player1.make_move()
            else:
                move = self.player2.make_move()

            if move is not None:
                if self.mark_valid_move(move[0], move[1]):
                    self.round_count += 1
                    win = self.check_win()
                    if win:
                        self.running = False
                        # winner's turn, x1, y1, x2, y2 are returned
                        return self.turn, win[0][0], win[0][1], win[1][0], win[1][1]
                    else:
                        if self.is_board_full():
                            self.running = False
                            return None
                        turn = 1 if turn == 2 else 1
                        sleep(0.3)
                        

    
    def finish_game(self):
        self.running = False