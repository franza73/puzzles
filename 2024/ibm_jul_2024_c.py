'''
IBM Ponder This June 2024
'''
import numpy as np


def _empty_board(n):
    m = 4 * n
    return np.matrix([[-1]*m]*m, dtype=int)


def equivalents(tile):
    '''
    For a given tile, find the 1, 2, 4 or 8 possible equivalent ones.
    '''
    flip = np.fliplr(tile)
    res = set()
    res.add(str(tile))
    res.add(str(flip))
    for rot in range(1, 4):
        res.add(str(np.rot90(tile, rot)))
        res.add(str(np.rot90(flip, rot)))
    return res


class Board:
    ''' Board '''
    # pylint: disable=too-few-public-methods
    def __init__(self, n, board=None):
        self.n = n
        if not board:
            self.m = _empty_board(n)
            self.k = 0
            self.score = 0
        else:
            self.m = np.copy(board.m)
            self.k = board.k
            self.score = board.score

    def print(self):
        ''' print '''
        print(self.m, self.score)


class TileBoardPuzzle:
    ''' TileBoardPuzzle '''
    def __init__(self, n, goal_score, rate):
        self.n = n
        self.best_score = goal_score + 1
        self.goal_score = goal_score
        self.rate = rate

    def backtrack(self, board, visited: set):
        '''
        Fill the board by backtracking
        '''
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        def pos(k):
            return ((k//16)//self.n)*4 + (k % 16)//4, \
                   ((k//16) % self.n)*4 + (k % 16) % 4

        def get_tile(k):
            x_p, y_p = pos(k-1)
            return board.m[(x_p-3):(x_p+1), (y_p-3):(y_p+1)]

        if self.best_score == self.goal_score or \
           board.score >= self.best_score:
            return
        if board.k > 0 and board.k % 16 == 0:
            tile = get_tile(board.k)
            if tile.sum() != 8 or str(tile) in visited or \
               board.score / board.k > self.rate:
                return
            eqs = equivalents(tile)
            if len(eqs) != 4:
                return
            for ei in eqs:
                visited.add(str(ei))
            if board.k == (4*self.n)**2:
                print(board.m, board.score)
                self.best_score = min(board.score, self.best_score)
                return
        x, y = pos(board.k)
        vals = [0, 1]
        flag_x = flag_y = False
        if x > 1 and board.m[x-1, y] == board.m[x-2, y]:
            flag_x = True
        if y > 1 and board.m[x, y-1] == board.m[x, y-2]:
            flag_y = True
        if flag_x and flag_y and board.m[x-1, y] != board.m[x, y-1]:
            return
        if flag_x:
            vals = [1 - board.m[x-1, y]]
        if flag_y:
            vals = [1 - board.m[x, y-1]]
        for val in vals:
            board_n = Board(board.n, board)
            board_n.k += 1
            board_n.m[x, y] = val
            # ------------ zero-cost tile intersections ----------------------
            if x > 0 and x % 4 == 0 and board_n.m[x-1, y] == board_n.m[x, y]:
                continue
            if y > 0 and y % 4 == 0 and board_n.m[x, y-1] == board_n.m[x, y]:
                continue
            # ----------------------------------------------------------------
            if x > 0 and board_n.m[x, y] == board_n.m[x-1, y]:
                board_n.score += 1
            if y > 0 and board_n.m[x, y] == board_n.m[x, y-1]:
                board_n.score += 1
            visited_n = visited.copy()
            self.backtrack(board_n, visited_n)

    def solve(self):
        ''' solve the puzzle '''
        self.backtrack(Board(5), set())


TileBoardPuzzle(5, 184, 0.462).solve()
