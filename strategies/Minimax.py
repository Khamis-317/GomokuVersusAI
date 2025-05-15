directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
class Minimax:
    def __init__(self,cSize,rSize,depth,AI_PLAYER = 2):
        self.cSize = cSize
        self.rSize = rSize
        self.maxDepth = depth
        self.AI_PLAYER = AI_PLAYER
        self.HUMAN_PLAYER = 1 if AI_PLAYER == 2 else 2
    
    
    #O(M * N) * 3 -> O(M * N)  
    def is_terminal(self, board) -> None:
        return self.check_win(board,self.AI_PLAYER) != 0 or self.check_win(board,self.HUMAN_PLAYER) != 0 or not self.getAllAvaliableMove(board)
    
    #O(M*N) -> O(MN)
    def check_win(self,board,player) -> bool:
        for i in range(self.rSize):
            for j in range(self.cSize):
                if board[i][j] != player:
                    continue
                for dr, dc in directions:
                    if self.is_5_in_a_row(board, i, j, dr, dc, player): #O(c)
                        return True
        return False
        
    #O(c)
    def is_5_in_a_row(self, board, row, col, dr, dc,player):
        count = 0
        for k in range(5):
            r, c = row + dr * k, col + dc * k
            if 0 <= r < self.rSize and 0 <= c < self.cSize and board[r][c] == player:
                count += 1
            else:
                break
        return True if count == 5 else False
    
    #O(c)
    def evaluate_heuristic(self , count,  open_ends) -> int:
        if count == 5:
            return 1000000000
        if count == 4:
            return 10000000 if open_ends == 2 else 5000
        if count == 3:
            return 1000 if open_ends == 2 else 300
        if count == 2:
            return 100 if open_ends == 2 else 30
        if count == 1:
            return 10
        return 0
   
    def evaluate_score(self, board):
        return  self.evaluate_player(board, self.AI_PLAYER) - 1 * self.evaluate_player(board, self.HUMAN_PLAYER)

    def evaluate_player(self, board, player) -> int:
        total_score = 0
        for i in range(self.rSize):
            for j in range(self.cSize):
                if board[i][j] != player:
                    continue
                for dr, dc in directions:
                    count, open_ends = self.count_and_open_ends(board, i, j, dr, dc, player)
                    total_score += self.evaluate_heuristic(count, open_ends)
        return total_score

    def count_and_open_ends(self, board, r, c, dr, dc, player):
        count = 0
        i = 0
        while i < 5:
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < self.rSize and 0 <= nc < self.cSize and board[nr][nc] == player:
                count += 1
                i += 1
            else:
                break

        open_ends = 0
        before_r, before_c = r - dr, c - dc
        after_r, after_c = r + dr * count, c + dc * count
        if 0 <= before_r < self.rSize and 0 <= before_c < self.cSize and board[before_r][before_c] == 0:
            open_ends += 1
        if 0 <= after_r < self.rSize and 0 <= after_c < self.cSize and board[after_r][after_c] == 0:
            open_ends += 1

        return count, open_ends

    dir = [(1,0),(0,1),(1,1),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    #O(cSize * rSize) -> O(M * N)  
    def getAllAvaliableMove(self,board):
        #Return avaliable move
        list = []
        empty = [(i, j) for i in range(self.rSize)for j in range(self.cSize) if board[i][j] == 0]
        for i in range(self.rSize):
            for j in range(self.cSize):
                if(board[i][j] == 0):
                    for k,l in self.dir:
                        ni,nj = i+k,j+l
                        if(0<=ni<self.rSize and 0<=nj<self.cSize and board[ni][nj]!= 0):
                            list.append((i,j))
                            break
        return list if list else empty                                         
        
    def minimax_algo(self, board, maxPlayer, depth):
    # Terminal node or depth reached
        if self.is_terminal(board) or depth == 0:
            return (self.evaluate_score(board), (None, None))

        best_move = (None, None)

        if maxPlayer:
            maxEval = float('-inf')
            for move in self.getAllAvaliableMove(board):
                board[move[0]][move[1]] = self.AI_PLAYER  # Player 1
                eval_score, _ = self.minimax_algo(board, False, depth - 1)
                board[move[0]][move[1]] = 0  # Undo move

                if eval_score > maxEval:
                    maxEval = eval_score
                    best_move = move

            return (maxEval, best_move)

        else:
            minEval = float('inf')
            for move in self.getAllAvaliableMove(board):
                board[move[0]][move[1]] = self.HUMAN_PLAYER  
                eval_score, _ = self.minimax_algo(board, True, depth - 1)
                board[move[0]][move[1]] = 0  # Undo move

                if eval_score < minEval:
                    minEval = eval_score
                    best_move = move

            return (minEval, best_move)
    def make_move(self, board):
        #for MN
        _, move = self.minimax_algo(board, False, self.maxDepth) 
        return move

####################################################
class GomokuGame:
    def __init__(self, rows=15, cols=15, depth=4):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.ai = Minimax(cols, rows, depth)

    def display_board_with_emojis(self):
        print("   " + " ".join(f"{i:2}" for i in range(self.cols)))
        for i, row in enumerate(self.board):
            line = f"{i:2} "
            for cell in row:
                if cell == 0:
                    line += "⬜ "
                elif cell == 1:
                    line += "❌ "
                elif cell == 2:
                    line += "⭕ "
            print(line)
    def play(self):
        print("Welcome to Gomoku!")
        print("You are '⭕' (Human), AI is '❌'")
        human_player = 1
        ai_player = 2
        current_player = human_player

        while True:
            self.display_board_with_emojis()
            if self.ai.is_terminal(self.board):
                if self.ai.check_win(self.board, ai_player):
                    print("❌ AI wins!")
                elif self.ai.check_win(self.board, human_player):
                    print("⭕ Human wins!")
                else:
                    print("It's a draw!")
                break

            if current_player == human_player:
                try:
                    move = input("Enter your move as row,col (e.g. 3,4): ")
                    row, col = map(int, move.strip().split(','))
                    if not (0 <= row < self.rows and 0 <= col < self.cols):
                        print("Move out of bounds. Try again.")
                        continue
                    if self.board[row][col] != 0:
                        print("Cell is already occupied. Try again.")
                        continue
                    self.board[row][col] = human_player
                    current_player = ai_player
                except (ValueError, IndexError):
                    print("Invalid input. Try again.")
            else:
                print("AI is thinking...")
                move = self.ai.make_move(self.board)
                if move:
                    self.board[move[0]][move[1]] = ai_player
                    current_player = human_player
                else:
                    print("No moves left. Draw!")
                    break

if __name__ == "__main__":
    game = GomokuGame(rows=15, cols=15, depth=3)
    game.play()