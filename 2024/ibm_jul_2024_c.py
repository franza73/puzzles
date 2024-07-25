'''
IBM Ponder This June 2024
'''
# from random import shuffle
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


class TileBoardPuzzle:
    ''' TileBoardPuzzle '''
    def __init__(self, n, best_score, rate):
        self.n = n
        self.best_score = best_score
        self.rate = rate

    def backtrack(self, board, k, visited: set, score):
        '''
        Fill the board by backtracking
        '''
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-function-args
        # pylint: disable=too-many-branches
        def pos(k):
            return ((k//16)//self.n)*4 + (k % 16)//4, \
                   ((k//16) % self.n)*4 + (k % 16) % 4

        def get_tile(k):
            x_p, y_p = pos(k-1)
            return board[(x_p-3):(x_p+1), (y_p-3):(y_p+1)]

        if self.best_score == 184 or score >= self.best_score:
            return
        if k > 0 and k % 16 == 0:
            tile = get_tile(k)
            if tile.sum() != 8 or str(tile) in visited or \
               score / k > self.rate:
                return
            eqs = equivalents(tile)
            if len(eqs) != 4:
                return
            for ei in eqs:
                visited.add(str(ei))
            if k == (4*self.n)**2:
                print(board, score)
                self.best_score = min(score, self.best_score)
                return
        x, y = pos(k)
        vals = [0, 1]
        # shuffle(vals)
        flag_x = flag_y = False
        if x > 1 and board[x-1, y] == board[x-2, y]:
            flag_x = True
        if y > 1 and board[x, y-1] == board[x, y-2]:
            flag_y = True
        if flag_x and flag_y and board[x-1, y] != board[x, y-1]:
            return
        if flag_x:
            vals = [1 - board[x-1, y]]
        if flag_y:
            vals = [1 - board[x, y-1]]
        for val in vals:
            score_n = score
            board_n = np.copy(board)
            board_n[x, y] = val
            # ------------ zero-cost tile intersections ----------------------
            if x in set([4, 8, 12, 16]) and board_n[x-1, y] == board_n[x, y]:
                continue
            if y in set([4, 8, 12, 16]) and board_n[x, y-1] == board_n[x, y]:
                continue
            # ----------------------------------------------------------------
            if x > 0 and board_n[x, y] == board_n[x-1, y]:
                score_n += 1
            if y > 0 and board_n[x, y] == board_n[x, y-1]:
                score_n += 1
            visited_n = visited.copy()
            self.backtrack(self, board_n, k+1, visited_n, score_n)

    def solve(self):
        ''' solve the puzzle '''
        # pylint: disable=too-many-function-args
        self.backtrack(self, _empty_board(5), 0, set(), 0)
