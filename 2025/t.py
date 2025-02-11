'''
 1. numpy matrices, are these better?
 2. how much faster if we parallelize?

87 [[1, 7, 7, 7], [5, 5, 5, 7], [9, 3, 9, 1], [7, 7, 1, 7]]
104 [[7, 5, 7, 3], [7, 1, 7, 7], [5, 9, 5, 3], [3, 7, 3, 9]]
119 [[7, 5, 7, 3], [5, 1, 7, 9], [7, 9, 5, 1], [3, 7, 3, 9]]
128 [[7, 1, 7, 7], [5, 5, 5, 7], [9, 9, 3, 1], [1, 7, 7, 7]]
143 [[5, 7, 9, 1], [1, 7, 7, 7], [7, 5, 3, 7], [9, 3, 3, 7]]

'''
from collections import defaultdict
from copy import deepcopy
from sympy import isprime


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
    hist = defaultdict(int)
    for si in s:
        for sii in map(int, list(str(si))):
            hist[sii] += 1
    cost = 0
    for k, v in hist.items():
        cost += (v*(v-1)) // 2
    return cost


def solve(n):
    def fill(square, pos):
        x, y = pos
        if y == n:
            # full square
            full_cost = cost(square)
            diag = [0] * 2
            for i in range(n):
                diag[1] = diag[1] * 10 + square[i][n-i-1]
            if diag[1] in l22:
                full_cost = cost(square)
                if full_cost > 0: 
                    print(full_cost, square)
            return
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
        if x == 1 and y == n - 1:
            # FIXME if bottom_left of square
            opts_d2 = trie.search([square[i][n-i-1] for i in range(n-1)])
            #print('DEBUG', square, [square[i][n-i-1] for i in range(n-1)], opts_d2) 
            #opts = opts.intersection(opts_d2)
            #if not opts:
            #   return
        for opt in opts:
            n_square = deepcopy(square)
            n_square[x][y] = opt
            n_x, n_y = x + 1, y
            if n_x == n:
                n_x = 0
                n_y += 1
            fill(n_square, (n_x, n_y))

    # for a, list_of_primes in ...
    l22 = [1399, 1489, 1579, 1597, 1669, 1759, 1777, 1867, 1993, 2389, 2659, 2677, 2749, 2767, 2857, 3469, 3559, 3739, 3793, 3847, 3919, 4099, 4297, 4549, 4567, 4639, 4657, 4729, 4783, 4909, 5179, 5197, 5449, 5557, 5647, 5683, 5737, 5791, 5827, 5881, 5953, 6079, 6277, 6367, 6529, 6547, 6619, 6637, 6673, 6691, 6709, 6763, 6781, 6871, 6907, 6961, 7069, 7159, 7177, 7393, 7537, 7573, 7591, 7681, 7717, 7753, 7933, 7951, 8059, 8167, 8293, 8329, 8419, 8527, 8563, 8581, 8707, 8761, 8923, 8941, 9049, 9067, 9157, 9283, 9319, 9337, 9391, 9463, 9643, 9661, 9733, 9931]
    a = 22
    trie = PrimesTrie(l22)
    fill([[0 for i in range(n)] for j in range(n)], (0, 0))


if __name__ == "__main__":
    solve(4)
    #solve(5)
    #solve(6)