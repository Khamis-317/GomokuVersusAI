from movement import Movement

"""
class Alpha_Beta(Movement):
    def __init__(self, rows, columns, depth):
        self.ROWS, self.COLUMNS, self.DEPTH = rows, columns, depth

    def check_win(self, board, row, col, player):
        for dr, dc in directions:
            cnt = 0
            for i in range(5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                    cnt += 1
                else:
                    break
            if cnt == 5:
                return True
        return False

    def evaluate(self, board,maximizing) -> tuple:
        value = float("-inf")
        player = 2
        opp = 1
        if maximizing:
            player,opp = opp,player

        for i in range(self.COLUMNS):
            for j in range(self.ROWS):
                if board[i][j] != 0:
                    continue
                value = max(value,self.window_of_5(board,player,i,
                            j,0) - 0.8 * self.window_of_5(board,opp,i,j,0))

        return value

    def window_of_5(self, board, player, row, col, val) -> int:
        score = 0
        for i in range(-4, 1):
            r = row + i
            c = col
            window = []
            for j in range(5):
                r += j
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                    window.append(board[r][c])
                else:
                    break
            if len(window) == 5:
                player_count = window.count(player)
                empty_count = window.count(0)

                if player_count == 2 and empty_count == 3:
                    score = max(score,25)
                elif player_count == 3 and empty_count == 2:
                    score = max(50,score)
                elif player_count == 4 and empty_count == 1:
                    return 10000000000

        for j in range(-4, 1):
            c = col + j
            r = row
            window = []
            for i in range(5):
                c += i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                    window.append(board[r][c])
                else:
                    break
            if len(window) == 5:
                player_count = window.count(player)
                empty_count = window.count(0)

                if player_count == 2 and empty_count == 3:
                    score = max(score,25)
                elif player_count == 3 and empty_count == 2:
                    score = max(50,score)
                elif player_count == 4 and empty_count == 1:
                    return 10000000000
        for j in range(-4, 1):
            c = col + j
            r = row + j
            window = []
            for i in range(5):
                c += i
                r += i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                    window.append(board[r][c])
                else:
                    break
            if len(window) == 5:
                player_count = window.count(player)
                empty_count = window.count(0)

                if player_count == 2 and empty_count == 3:
                    score = max(score,25)
                elif player_count == 3 and empty_count == 2:
                    score = max(50,score)
                elif player_count == 4 and empty_count == 1:
                    return 10000000000
        for j in range(-4, 1):
            c = col + j
            r = row - j
            window = []
            for i in range(5):
                c -= i
                r += i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                    window.append(board[r][c])
                else:
                    break
            if len(window) == 5:
                player_count = window.count(player)
                empty_count = window.count(0)

                if player_count == 2 and empty_count == 3:
                    score = max(score,25)
                elif player_count == 3 and empty_count == 2:
                    score = max(50,score)
                elif player_count == 4 and empty_count == 1:
                    return 10000000000
        val += score
        return val

    def get_all_avaliable_move(self, board, maximizing):
        player = 1
        if maximizing:
            opp = 2
        else:
            opp = 1
            player = 2
        moves = [(i, j, -abs(i - self.ROWS*j//2) - abs(j - self.COLUMNS*i//2)) if i != self.ROWS//2 or j != self.COLUMNS //
                 2 else (i, j, 10000000) for i in range(self.ROWS) for j in range(self.COLUMNS) if board[i][j] == 0]
        moves.sort(key=lambda val: val[2], reverse=True)
        return moves

    def prune(self, board, alpha, beta, depth, maximizing_player) -> tuple:
        if depth == 0:
            return None,None,self.evaluate(board,maximizing_player)

        moves = self.get_all_avaliable_move(board, maximizing_player)

        if maximizing_player:
            maxEval = (0, 0, float('-inf'))
            for x, y, _ in moves[:5]:

                board[x][y] = 2
                currEval = self.prune(board, alpha, beta, depth - 1, 1)
                board[x][y] = 0
                if maxEval[2] < currEval[2]:
                    maxEval = x,y,currEval[2]
                alpha = max(alpha, maxEval[2])
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = (0, 0, float('inf'))
            for x, y, _ in moves[:5]:

                board[x][y] = 1
                currEval = self.prune(board, alpha, beta,depth - 1, 2)
                board[x][y] = 0
                if minEval[2] > currEval[2]:
                    minEval = x,y,currEval[2]

                beta = min(minEval[2], beta)
                if beta <= alpha:
                    break
            return minEval

    def make_move(self, board) -> tuple:
        temp_board = [row[:] for row in board]
        move = self.prune(temp_board, float('-inf'), float('inf'), 4, True)
        return move[0], move[1] """


import math

directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

class Alpha_Beta(Movement):

    def __init__(self, rows, columns, depth):
        self.ROWS, self.COLUMNS, self.DEPTH = rows, columns, depth

    def extract_line(self, board, row, col, dr, dc, length):
        line = []
        for i in range(length):
            r = row + i * dr
            c = col + i * dc
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                line.append(board[r][c])
            else:
                line.append(-1)
        return line

    def pattern_score(self, line, player):
        score = 0
        PATTERNS = {
            (0, player, player, player, player, 0): 100000,
            (player, player, player, player, 0):    50000,
            (0, player, player, player, 0):    10000,
            (player, player, 0, player):       5000,
            (0, player, player, 0):       1000,
            (player, player, 0):          100
        }
        for pattern, val in PATTERNS.items():
            L = len(pattern)
            for i in range(len(line) - L + 1):
                if tuple(line[i:i+L]) == pattern:
                    score += val
        return score

    def evaluate(self, board, maximizing) -> float:
        total = 0
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                if board[r][c] != 0 and self.check_win(board, r, c, board[r][c]):
                    return math.inf if board[r][c] == 2 else -math.inf
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                for dr, dc in directions:
                    line = self.extract_line(board, r - 5*dr, c - 5*dc, dr, dc, 11)
                    total += self.pattern_score(line, 2)
                    total -= self.pattern_score(line, 1) * 0.3
        return total

    def get_all_available_moves(self, board):
        moves = []
        center_r, center_c = self.ROWS // 2, self.COLUMNS // 2
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if board[i][j] == 0:
                    dist = abs(i - center_r) + abs(j - center_c)
                    moves.append((i, j, -dist))
        moves.sort(key=lambda x: x[2], reverse=True)
        return moves

    def prune(self, board, alpha, beta, depth, maximizing_player) -> tuple:
        if depth == 0:
            return None, None, self.evaluate(board, maximizing_player)
        best_move = (None, None, math.inf if not maximizing_player else -math.inf)
        for x, y, _ in self.get_all_available_moves(board)[:6]:
            board[x][y] = 2 if maximizing_player else 1
            _, _, eval_score = self.prune(board, alpha, beta, depth - 1, not maximizing_player)
            board[x][y] = 0
            if maximizing_player:
                if eval_score > best_move[2]: best_move = (x, y, eval_score)
                alpha = max(alpha, eval_score)
            else:
                if eval_score < best_move[2]: best_move = (x, y, eval_score)
                beta = min(beta, eval_score)
            if beta <= alpha: break
        return best_move

    def find_threat(self, board, player, length=4):
        """
        Find any `length`-in-a-row threat for `player` and return a winning/blocking cell.
        """
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                if board[r][c] != 0: continue
                board[r][c] = player
                if self.check_win(board, r, c, player):
                    board[r][c] = 0
                    return r, c
                board[r][c] = 0
        return None

    def find_weaker_threat(self, board, player, target_count=3):
        """
        Find any 5-cell window containing `target_count` stones of `player` and return an empty to block.
        """
        for dr, dc in directions:
            for r in range(self.ROWS):
                for c in range(self.COLUMNS):
                    for offset in range(5):
                        count = 0
                        empties = []
                        valid = True
                        for i in range(5):
                            rr = r + (offset + i) * dr
                            cc = c + (offset + i) * dc
                            if 0 <= rr < self.ROWS and 0 <= cc < self.COLUMNS:
                                val = board[rr][cc]
                                if val == player:
                                    count += 1
                                elif val == 0:
                                    empties.append((rr, cc))
                            else:
                                valid = False
                                break
                        if valid and count == target_count and empties:
                            return empties[0]
        return None

    def make_move(self, board) -> tuple:
        # 1. Win if possible
        move = self.find_threat(board, 2)
        if move: return move
        # 2. Block opponent's immediate win
        move = self.find_threat(board, 1)
        if move: return move
        # 3. Block opponent's 4-in-a-row
        move = self.find_weaker_threat(board, 1, 4)
        if move: return move
        # 4. Block opponent's open 3-in-a-row (0,1,1,1,0)
        for dr, dc in directions:
            for r in range(self.ROWS):
                for c in range(self.COLUMNS):
                    for offset in range(3):  # check 5-window offsets 0-2
                        seq = []
                        for i in range(5):
                            rr = r + (offset + i) * dr
                            cc = c + (offset + i) * dc
                            seq.append(board[rr][cc] if 0 <= rr < self.ROWS and 0 <= cc < self.COLUMNS else -1)
                        if tuple(seq) == (0,1,1,1,0):
                            # block either end
                            start = (r + offset * dr, c + offset * dc)
                            end = (r + (offset + 4) * dr, c + (offset + 4) * dc)
                            return start if board[start[0]][start[1]] == 0 else end
        # 5. Block opponent's 3-in-a-row setup (generic)
        #move = self.find_weaker_threat(board, 1, 3)
        if move: return move
        # 6. Otherwise alpha-beta
        r, c, _ = self.prune([row[:] for row in board], -math.inf, math.inf, self.DEPTH, True)
        return r, c #Otherwise alpha-beta



    def count_sequence(self, board, row, col, dr, dc, player):
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        return count

    def check_win(self, board, row, col, player):
        for dr, dc in directions:
            if self.count_sequence(board, row, col, dr, dc, player) >= 5:
                return True
        return False


""" 
from movement import Movement, directions

class Alpha_Beta(Movement):
    def __init__(self, rows, columns, depth):
        self.ROWS, self.COLUMNS, self.DEPTH = rows, columns, depth
        self.heuristic = [[0 for _ in range(columns)] for _ in range(rows)]
        self.initialize_heuristic()

    def count_sequence(self, board, row, col, dr, dc, player):
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        return count

    def check_win(self, board, row, col, player):
        for dr, dc in directions:
            if self.count_sequence(board, row, col, dr, dc, player) >= 5:
                return True
        return False

    def evaluate(self, board) -> tuple:
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                player = board[i][j]
                if player == 0:
                    continue
                if self.check_win(board, i, j, player):
                    return (1000000000, (i, j)) if player == 1 else (-1000000000, (i, j))
        return (0, (None,None))

    def update_heuristic(self, board, current_player):
        opp_player = 2 if current_player == 1 else 1
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                self.window_of_5(board, current_player, opp_player, i, j)

    def window_of_5(self, board, player, opp, row, col) -> None:
        for dr, dc in directions:
            window = []
            for i in range(5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                    window.append(board[r][c])
                else:
                    break
            if len(window) == 5:
                player_count = window.count(player)
                opp_count = window.count(opp)
                empty_count = window.count(0)
                if player_count == 2 and empty_count == 3:
                    self.heuristic[row][col] += 250
                elif player_count == 3 and empty_count == 2:
                    self.heuristic[row][col] += 400
                elif player_count == 4 and empty_count == 1:
                    self.heuristic[row][col] += 950
                if opp_count == 2 and empty_count == 3:
                    self.heuristic[row][col] -= 150
                elif opp_count == 3 and empty_count == 2:
                    self.heuristic[row][col] -= 255
                elif opp_count == 4 and empty_count == 1:
                    self.heuristic[row][col] -= 310

    def getAllAvaliableMove(self, board):
        return [(i, j) for i in range(self.ROWS) for j in range(self.COLUMNS) if board[i][j] == 0]

    def copy_heuristic(self):
        return [row[:] for row in self.heuristic]

    def is_terminal(self, board):
        return self.evaluate(board)[0] != 0 or not self.getAllAvaliableMove(board)

    def prune(self, board, alpha, beta, depth, maximizing_player) -> tuple:
        if self.is_terminal(board):
            return self.evaluate(board)

        moves = self.getAllAvaliableMove(board)
        moves.sort(key=lambda x: self.heuristic[x[0]][x[1]], reverse=maximizing_player)

        if depth == 0:
            return self.heuristic[moves[0][0]][moves[0][1]], moves[0]

        if maximizing_player:
            maxEval = (float('-inf'), (0, 0))
            for move in moves:
                board[move[0]][move[1]] = 2
                curr_heuristic = self.copy_heuristic()
                self.update_heuristic(board, 2)
                currEval = self.prune(board, alpha, beta, depth - 1, False)
                self.heuristic = curr_heuristic
                board[move[0]][move[1]] = 0
                if maxEval[0] < currEval[0]:
                    maxEval = currEval
                alpha = max(alpha, maxEval[0])
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = (float('inf'), (0, 0))
            for move in moves:
                board[move[0]][move[1]] = 1
                curr_heuristic = self.copy_heuristic()
                self.update_heuristic(board, 1)
                currEval = self.prune(board, alpha, beta, depth - 1, True)
                self.heuristic = curr_heuristic
                board[move[0]][move[1]] = 0
                if minEval[0] > currEval[0]:
                    minEval = currEval
                beta = min(beta, minEval[0])
                if beta <= alpha:
                    break
            return minEval

    def initialize_heuristic(self):
        center_i = self.ROWS // 2
        center_j = self.COLUMNS // 2
        max_value, decay_rate, min_value = (self.ROWS * self.COLUMNS) // 2, 3, 1
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                distance = abs(i - center_i) + abs(j - center_j)
                value = max(max_value - decay_rate * distance, min_value)
                self.heuristic[i][j] = value


    def make_move(self, board) -> tuple:
        temp_board = [row[:] for row in board]
        return self.prune(temp_board, float('-inf'), float('inf'), self.DEPTH, True)
        
        
        
 from movement import Movement, directions

class Alpha_Beta(Movement):
    def __init__(self, rows, columns, depth):
        self.ROWS, self.COLUMNS, self.DEPTH = rows, columns, depth
        self.memo = {}

    def count_sequence(self, board, row, col, dr, dc, player):
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and board[r][c] == player:
                count += 1
            else:
                break
        return count

    def check_win(self, board, row, col, player):
        for dr, dc in directions:
            if self.count_sequence(board, row, col, dr, dc, player) >= 5:
                return True
        return False

    def evaluate_board(self, board):
        score = 0
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if board[i][j] == 0:
                    continue
                player = board[i][j]
                for dr, dc in directions:
                    count = 1
                    open_ends = 0
                    for step in range(1, 5):
                        r, c = i + dr * step, j + dc * step
                        if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS:
                            if board[r][c] == player:
                                count += 1
                            elif board[r][c] == 0:
                                open_ends += 1
                                break
                            else:
                                break
                    score_delta = 0
                    if count == 5:
                        return 1000000000 if player == 1 else -1000000000
                    if player == 2:
                        score_delta = 10 * count if open_ends > 0 else 0
                    else:
                        score_delta = -(10 * count) if open_ends > 0 else 0
                    score += score_delta
        return score

    def getAllAvaliableMove(self, board):
        moves = set()
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if board[i][j] != 0:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            ni, nj = i + dx, j + dy
                            if 0 <= ni < self.ROWS and 0 <= nj < self.COLUMNS and board[ni][nj] == 0:
                                moves.add((ni, nj))
        return list(moves)

    def is_terminal(self, board):
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if board[i][j] != 0 and self.check_win(board, i, j, board[i][j]):
                    return True
        return not self.getAllAvaliableMove(board)

    def board_hash(self, board):
        return tuple(tuple(row) for row in board)

    def prune(self, board, alpha, beta, depth, maximizing_player):
        board_key = (self.board_hash(board), depth, maximizing_player)
        if board_key in self.memo:
            return self.memo[board_key]

        if self.is_terminal(board) or depth == 0:
            score = self.evaluate_board(board)
            best_move = (None, None)
            for i in range(self.ROWS):
                for j in range(self.COLUMNS):
                    if board[i][j] == 0:
                        best_move = (i, j)
                        break
                if best_move != (None, None):
                    break
            self.memo[board_key] = (score, best_move)
            return (score, best_move)

        moves = self.getAllAvaliableMove(board)
        best_move = moves[0]

        if maximizing_player:
            maxEval = float('-inf')
            for move in moves:
                board[move[0]][move[1]] = 2
                eval_score = self.prune(board, alpha, beta, depth - 1, False)[0]
                board[move[0]][move[1]] = 0
                if eval_score > maxEval:
                    maxEval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.memo[board_key] = (maxEval, best_move)
            return (maxEval, best_move)
        else:
            minEval = float('inf')
            for move in moves:
                board[move[0]][move[1]] = 1
                eval_score = self.prune(board, alpha, beta, depth - 1, True)[0]
                board[move[0]][move[1]] = 0
                if eval_score < minEval:
                    minEval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.memo[board_key] = (minEval, best_move)
            return (minEval, best_move)

    def make_move(self, board) -> tuple:
        temp_board = [row[:] for row in board]
        num_moves = len(self.getAllAvaliableMove(temp_board))
        depth = self.DEPTH if num_moves < 15 else max(1, self.DEPTH - 1)
        return self.prune(temp_board, float('-inf'), float('inf'), depth, True)
 """
