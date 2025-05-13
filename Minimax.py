class Minimax:
    def __init__(self,cSize,rSize,depth):
        self.cSize = cSize
        self.rSize = rSize
        self.maxDepth = depth
    
    
    #O(M * N) * 2 -> O(M * N)  
    def is_terminal(self, board):
        return self.evaluate(board) != 0 or not self.getAllAvaliableMove(board)
    
    #O(8*5) -> O(C)
    def check_win(self,board,row,col,player):
        dx = [1,0,1,1,0,-1,-1,-1]
        dy = [0,1,1,-1,-1,-1,0,1]
        #Check 8 directionss
        #(-1,-1) | ( 0,-1) | ( 1,-1)
        #(-1, 0) | ( 0, 0) | ( 1, 0)
        #(-1, 1) | ( 0, 1) | (-1, 1)
        
        for dr,dc in zip(dx,dy):
            # In each direction check 5 cells One after the other
            cnt = 0
            for i in range(5):
                r,c = row + dr * i , col + dc * i    
                if 0 <= r <self.rSize and 0 <= c < self.cSize and board[r][c] == player:
                    cnt += 1
                else:
                    break
            if cnt == 5:
                return True
        return False
    #O(cSize * rSize) -> O(M * N)  
    def evaluate(self, board):
        #Return  2  in case AI won
        #Return  0  in case  draw or nothing
        #Return -2  in case Human won
        for i in range(self.cSize):
            for j in range(self.rSize):
                player = board[i][j]
                if player == 0 :
                    continue
                if self.check_win(board,i,j,player):
                   return 2 if player == 1 else -2
        return 0 
    
    #O(cSize * rSize) -> O(M * N)  
    def getAllAvaliableMove(self,board):
        #Return avaliable move
        return [(i, j) for i in range(self.rSize) for j in range(self.cSize) if board[i][j] == 0]
        
    def minimax_algo(self,board,maxPlayer,depth):
        #O(M * N)^2
        if(self.is_terminal(board) or depth == 0): #O(M * N)  
            return self.evaluate(board) #O(M * N)  
        if(maxPlayer):
            maxEval = float('-inf')
            for move in self.getAllAvaliableMove(board):
                # branching factor -> O(M * N)
                board[move[0]][move[1]] = 1 #Do move
                currEval = self.minimax_algo(board, False, depth-1) #backtrack 
                board[move[0]][move[1]] = 0 #Undo
                maxEval = max(currEval,maxEval)
            return maxEval
        else:
            minEval = float('inf')
            for move in self.getAllAvaliableMove(board):
                board[move[0]][move[1]] = -1
                currEval = self.minimax_algo(board, True , depth-1)
                board[move[0]][move[1]] = 0
                minEval = min(minEval,currEval)
            return minEval        
        
    def make_move(self,board):
        best_val = float('-inf')
        best_move = None
        for move in self.getAllAvaliableMove(board): #O(M * N)  
            board[move[0]][move[1]] = 1;
            move_val = self.minimax_algo(board,False,self.maxDepth)
            board[move[0]][move[1]] = 0;
            if move_val > best_val:
                best_val = move_val
                best_move = move
        return best_move

