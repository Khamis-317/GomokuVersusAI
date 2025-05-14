directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
class Minimax:
    def __init__(self,cSize,rSize,depth):
        self.cSize = cSize
        self.rSize = rSize
        self.maxDepth = depth
    
    
    #O(M * N) * 3 -> O(M * N)  
    def is_terminal(self, board) -> None:
        return self.check_win(board,1) != 0 or self.check_win(board,-1) != 0 or not self.getAllAvaliableMove(board)
    
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
            return 100000
        if count == 4:
            return 10000 if open_ends == 2 else 5000
        if count == 3:
            return 1000 if open_ends == 2 else 300
        if count == 2:
            return 100 if open_ends == 2 else 30
        if count == 1:
            return 10
        return 0
    
    def evaluate_score(self, board):
        return self.evaluate_player(board, 1) - self.evaluate_player(board, -1)

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

    def score_sequence(self, count, open_ends):
        if count >= 5:
            return 10000
        if count == 4:
            return 10000 if open_ends == 2 else 5000
        if count == 3:
            return 2000 if open_ends == 2 else 1000
        if count == 2:
            return 300 if open_ends == 2 else 30
        if count == 1:
            return 10
        return 0

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

    
    #O(cSize * rSize) -> O(M * N)  
    def getAllAvaliableMove(self,board):
        #Return avaliable move
        return [(i, j) for i in range(self.rSize) for j in range(self.cSize) if board[i][j] == 0]
        
    def minimax_algo(self, board, maxPlayer, depth):
    # Terminal node or depth reached
        if self.is_terminal(board) or depth == 0:
            return (self.evaluate_score(board), (None, None))

        best_move = (None, None)

        if maxPlayer:
            maxEval = float('-inf')
            for move in self.getAllAvaliableMove(board):
                board[move[0]][move[1]] = 1  # Player 1
                eval_score, _ = self.minimax_algo(board, False, depth - 1)
                board[move[0]][move[1]] = 0  # Undo move

                if eval_score > maxEval:
                    maxEval = eval_score
                    best_move = move

            return (maxEval, best_move)

        else:
            minEval = float('inf')
            for move in self.getAllAvaliableMove(board):
                board[move[0]][move[1]] = -1  # Player -1
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

