'''
 1. numpy matrices, are these better?
 2. how much faster if we parallelize?

For A = 22:
87 [[1, 7, 7, 7], [5, 5, 5, 7], [9, 3, 9, 1], [7, 7, 1, 7]]
104 [[7, 5, 7, 3], [7, 1, 7, 7], [5, 9, 5, 3], [3, 7, 3, 9]]
119 [[7, 5, 7, 3], [5, 1, 7, 9], [7, 9, 5, 1], [3, 7, 3, 9]]
128 [[7, 1, 7, 7], [5, 5, 5, 7], [9, 9, 3, 1], [1, 7, 7, 7]]
143 [[5, 7, 9, 1], [1, 7, 7, 7], [7, 5, 3, 7], [9, 3, 3, 7]]

'''
from collections import defaultdict
from copy import deepcopy
from sympy import isprime
import concurrent.futures
from random import shuffle


class PrimesTrie:
    def __init__(self, primes_list):
        self.root = dict()
        for li in primes_list:
            self.curr = self.root
            for lii in list(map(int, list(str(li)))):
                self.curr = self.curr.setdefault(lii, {})
            self.curr['_end_'] = '_end_'

    def search(self, partial):
        curr = self.root
        for d in partial:
            if d not in curr:
                return set()
            curr = curr[d]
        return set(curr.keys())


def first_square(prime):
    n = len(str(prime))
    m = [[-1] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        m[i][n-i-1] = prime % 10
        prime //= 10
    return m

def cost(m):
    n = len(m)
    hor = [0] * n
    ver = [0] * n
    diag = [0] * 2
    for i in range(n):
        diag[0] = diag[0] * 10 + m[i][i]
        diag[1] = diag[1] * 10 + m[i][n-i-1]
        for j in range(n):
            hor[i] = hor[i] * 10 + m[i][j]
            ver[j] = ver[j] * 10 + m[i][j]
    s = set(hor).union(set(ver)).union(set(diag))
    _len_s = len(s)
    # Peace of mind... recheck the primes.
    for si in s:
       if not isprime(si):
           return -1, _len_s
    hist = defaultdict(int)
    for si in s:
        for sii in map(int, list(str(si))):
            hist[sii] += 1
    cost = 0
    for k, v in hist.items():
        cost += (v*(v-1)) // 2
    return cost, _len_s


def solve_parallel(args):
    n, a, trie, p1 = args

    def fill(square, pos):
        x, y = pos
        if y == n:
            # full square
            full_cost, len_s = cost(square)
            if full_cost != -1 and full_cost < 180:
                print(full_cost, len_s, a, square)
            return
        if square[x][y] != -1:
            n_x, n_y = x + 1, y
            if n_x == n:
                n_x = 0
                n_y += 1
            fill(square, (n_x, n_y))
            return
        opts = set()
        opts_x = trie.search([square[x][j] for j in range(y)])
        if not opts_x:
            return
        opts_y = trie.search([square[i][y] for i in range(x)])
        if not opts_y:
            return
        opts = opts_x.intersection(opts_y)
        # if x == y:
        #     opts_d1 = trie.search([square[i][i] for i in range(x)])
        #     opts = opts.intersection(opts_d1)
        #     if not opts:
        #         return
        for opt in opts:
            n_square = deepcopy(square)
            n_square[x][y] = opt
            # symmetrical
            if x != y and n_square[y][x] == -1:
                n_square[y][x] = opt
            n_x, n_y = x + 1, y
            if n_x == n:
                n_x = 0
                n_y += 1
            fill(n_square, (n_x, n_y))
    print('Starting', a, p1)
    fill(first_square(p1), (0, 0))


def solve(n):
    # For each value of a in increasing order, find the squares with primes
    H = defaultdict(list)
    for p in range(10**(n-1), 10**n):
        if isprime(p):
            A = sum(map(int, list(str(p))))
            H[A] += [p]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        todo = []
        for a in sorted(H.keys()):
            if a not in set([26]):
               continue            
            primes = H[a]
            trie = PrimesTrie(primes)
            for p1 in primes:
                cnt = 0
                for x, y in zip(str(p1), str(p1)[::-1]):
                    if x != y:
                        cnt += 1
                if cnt == 2:
                    todo += [(n, a, trie, p1)]
        shuffle(todo)
        for res in executor.map(solve_parallel, todo):
            pass


if __name__ == "__main__":
    # solve(4)
    # solve(5)
    solve(6)
