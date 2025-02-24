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
from collections import Counter


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
    # Peace of mind... TODO: remove
    # for si in s:
    #    if not isprime(si):
    #        return -1
    hist = defaultdict(int)
    for si in s:
        for sii in map(int, list(str(si))):
            hist[sii] += 1
    cost = 0
    for k, v in hist.items():
        cost += (v*(v-1)) // 2
    return cost


def solve_parallel(args):
    n, a, primes = args

    def fill(square, pos, hist, index):
        x, y = pos
        if y == n:
            # full square
            full_cost = cost(square)
            print(full_cost, a, square)
            return
        # TEMP: exclude dense squares
        if index > 6:
            d_cost = sum([(v*(v-1)) // 2 for v in hist.values()])
            if d_cost / index**2 < 0.84:
                return
            # if index <= 30 and d_cost > 350:
            #     return
        opts = set()
        opts_x = trie.search([square[x][j] for j in range(y)])
        if not opts_x:
            return
        opts_y = trie.search([square[i][y] for i in range(x)])
        if not opts_y:
            return
        opts = opts_x.intersection(opts_y)
        if x == y:
            opts_d1 = trie.search([square[i][i] for i in range(x)])
            opts = opts.intersection(opts_d1)
            if not opts:
                return
        if x == 1 and y == n-1 and square[0][n-1] > 0:
            # Cut short if secondary diagonal was filled with non prime
            opts_d2 = trie.search([square[i][n-i-1] for i in range(n)])
            if not opts_d2:
                return
        #for _, opt in sorted((hist[opt], opt) for opt in opts):
        for opt in opts:
            n_square = deepcopy(square)
            n_square[x][y] = opt
            n_hist = Counter(hist)
            n_hist[opt] += 3 if (x == y or x+y == n-1) else 2
            n_x, n_y = x + 1, y
            if n_x == n:
                n_x = 0
                n_y += 1
            fill(n_square, (n_x, n_y), n_hist, index + 1)

    trie = PrimesTrie(primes)
    fill([[0 for i in range(n)] for j in range(n)], (0, 0), Counter(), 0)


def solve(n):
    # For each value of a in increasing order, find the squares with primes
    H = defaultdict(list)
    for p in range(10**(n-1), 10**n):
        if isprime(p):
            A = sum(map(int, list(str(p))))
            H[A] += [p]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        todo = ((n, a, H[a]) for a in sorted(H.keys()))
        for res in executor.map(solve_parallel, todo):
            pass


if __name__ == "__main__":
    #solve(4)
    # solve(5)
    solve(6)
