'''
IBM Ponder This June 2024
'''
import numpy as np
from random import shuffle


def empty_board(n):
    M = 4 * n
    return np.matrix([[-1]*M]*M, dtype=int)


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


def backtrack(board, k, visited: set, score):
    global best_score
    def pos(k):
        return ((k//16)//N)*4 + (k%16)//4, ((k//16)%N)*4 + (k%16)%4
    if score >= best_score:
        return
    if best_score == 284:
        return
    if k > 0 and k % 16 == 0:
        x_p, y_p = pos(k-1)
        tile = board[(x_p-3):(x_p+1),(y_p-3):(y_p+1)]
        if tile.sum() != 8:
            return
        if str(tile) in visited:
            return
        # -- TODO 1 ---------
        if score / k > 0.462:
            return
        # -------------------
        eqs = equivalents(tile)
        if len(eqs) != 4:
            return
        for ei in eqs:
            visited.add(str(ei))
        if k == (4*N)**2:
            print(board, score)
            best_score = min(score, best_score)
            return
    x, y = pos(k)
    vals = [0, 1]
    shuffle(vals)
    flag_x = flag_y = False
    if x > 1 and board[x-1, y] == board[x-2, y]:
        flag_x = True
    if y > 1 and board[x, y-1] == board[x, y-2]:
        flag_y = True
    if flag_x and flag_y and board[x-1, y] != board[x, y-1]:
        return
    elif flag_x:
        vals = [1 - board[x-1, y]]
    elif flag_y:
        vals = [1 - board[x, y-1]]
    for val in vals:
        score_n = score
        board_n = np.copy(board)
        board_n[x, y] = val
        # -- TODO 2 -- zero-cost tile intersections --------------------------
        if x in set([4, 8, 12, 16]) and board_n[x-1, y] == board_n[x, y]:
            continue
        elif y in set([4, 8, 12, 16]) and board_n[x, y-1] == board_n[x, y]:
            continue
        # --------------------------------------------------------------------
        if x > 0 and board_n[x, y] == board_n[x-1, y]:
            score_n += 1
        if y > 0 and board_n[x, y] == board_n[x, y-1]:
            score_n += 1
        visited_n = visited.copy()
        backtrack(board_n, k+1, visited_n, score_n)


N = 5
best_score = 185
backtrack(empty_board(N), 0, set(), 0)
