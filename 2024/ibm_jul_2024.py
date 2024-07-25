''' IBM Ponder This July 2024 '''
import numpy as np


def equivalents(tile):
    ''' Find the 1, 2, 4 or 8 possible equivalent tiles '''
    flip = np.fliplr(tile)
    res = set()
    res.add(str(tile))
    res.add(str(flip))
    for rot in range(1, 4):
        res.add(str(np.rot90(tile, rot)))
        res.add(str(np.rot90(flip, rot)))
    return res


class Board:
    ''' Board of tiles '''
    def __init__(self, n, board=None):
        self.n = n
        if not board:
            self.m = np.matrix([[-1]*4*n]*4*n, dtype=int)
            self.k = 0
            self.score = 0
        else:
            self.m = np.copy(board.m)
            self.k = board.k
            self.score = board.score

    def _pos(self, k):
        ''' Fills a complete tile at a time '''
        return ((k//16)//self.n)*4 + (k % 16)//4, \
               ((k//16) % self.n)*4 + (k % 16) % 4

    def pos(self):
        ''' Current x, y position '''
        return self._pos(self.k)

    def print(self):
        ''' Print the board '''
        print(self.m, self.score)

    def last_tile(self):
        ''' Last filled tile of the board '''
        xp, yp = self._pos(self.k-1)
        return self.m[(xp-3):(xp+1), (yp-3):(yp+1)]


class TileBoardPuzzle:
    ''' Solves the board tiling problem using backtracking '''
    def __init__(self, n, goal_score, rate, star=False) -> None:
        self.n = n
        self.best_score = goal_score + 1
        self.goal_score = goal_score
        self.rate = rate
        self.star = star

    def backtrack(self, board, visited: set):
        ''' Backtrack the whole board '''
        def _vals():
            vals = [0, 1]
            flag_x = flag_y = False
            if x > 1 and board.m[x-1, y] == board.m[x-2, y]:
                flag_x = True
            if y > 1 and board.m[x, y-1] == board.m[x, y-2]:
                flag_y = True
            if flag_x and flag_y and board.m[x-1, y] != board.m[x, y-1]:
                return []
            if flag_x:
                vals = [1 - board.m[x-1, y]]
            if flag_y:
                vals = [1 - board.m[x, y-1]]
            return vals

        if self.best_score == self.goal_score or \
           board.score >= self.best_score:
            return
        if board.k > 0 and board.k % 16 == 0:
            tile = board.last_tile()
            if tile.sum() != 8 or \
               str(tile) in visited or \
               board.score / board.k > self.rate:
                return
            eqs = equivalents(tile)
            if self.star and len(eqs) != 4:
                return
            for ei in eqs:
                visited.add(str(ei))
            if board.k == (4*self.n)**2:
                board.print()
                self.best_score = min(board.score, self.best_score)
                return
        x, y = board.pos()

        for val in _vals():
            board_n = Board(board.n, board)
            board_n.k += 1
            board_n.m[x, y] = val
            # -------------- no-cost tile intersections --------------------
            if x > 0 and x % 4 == 0 and board_n.m[x-1, y] == board_n.m[x, y]:
                continue
            if y > 0 and y % 4 == 0 and board_n.m[x, y-1] == board_n.m[x, y]:
                continue
            # --------------------------------------------------------------
            if x > 0 and board_n.m[x, y] == board_n.m[x-1, y]:
                board_n.score += 1
            if y > 0 and board_n.m[x, y] == board_n.m[x, y-1]:
                board_n.score += 1
            visited_n = visited.copy()
            self.backtrack(board_n, visited_n)

    def solve(self):
        ''' Solve the problem '''
        self.backtrack(Board(self.n), set())


# Problem 1
#
# Best choice of tiles to fill a 4x4 board.
#
# score   # of tiles
# -----   --------------------------------------------------------------------
# 0       1        There is 1 tile of score 0
# 3       2        There are 2 tiles of score 3
# 4       3+3 = 6  There are 3 tiles of score 4 with 4 equivalents and
#                  There are 3 tiles of score 4 with 8 equivalents
# 5       6        There are 6 tiles of score 5
# 6       1        We need one tile of score 6 to make the 4x4 total
#        --
#        16        Total number of tiles
#
# With no cost tiling, the total score of the board is:
# 1*0 + 2*3 + 6*4 + 6*5 + 1*6 = 0 + 6 + 24 + 30 + 6 = 66

TileBoardPuzzle(4, 66, 0.259).solve()

# Problem 2
#
# Best choice for tiles to fill a 5x5 board with tiles that are 4-equivalent.
#
# score   # of tiles
# -----   --------------------------------------------------------------------
#  4      3        There are 3 tiles of score 4
#  6      8        There are 8 tiles of score 6
#  8      8        There are 8 tiles of score 8
# 10      6        We need 6 more tiles of score 10 to make the 5x5 total.
#        --
#        25
#
# With no cost tiling, the total score of the board is:
# 3*4 + 8*6 + 8*8 + 6*10 = 184

TileBoardPuzzle(5, 184, 0.462, True).solve()
