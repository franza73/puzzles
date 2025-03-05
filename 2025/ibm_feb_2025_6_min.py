'''
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


def solve_parallel(args):
    n, a, primes = args
    profile_min = {12: 7, 18: 16, 24: 26, 30: 48, 31: 66, 32: 95, 33: 119, 34: 157, 35: 157, 36: 192}
    def fill(square, pos, hist, index, set_of_primes, _cost, _non_symmetry_cost):
        x, y = pos
        # FIXME trim the bad non symmetric partial squares.
        if _non_symmetry_cost > 3 or _cost > 192:
            print(index)
            return
        # FIXME __MIN__ coefficient: 1.2, for 12 and 1.0 for 36 
        if index in profile_min:
            #if _cost > int((1.3 - index / 120.0) * profile_min[index] + 0.5):
            if _cost > profile_min[index]:
                return
        if y == n:
            # full square
            print(_cost, a, _non_symmetry_cost, square)
            return
        opts = set()
        #if x != y:
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
        if square[x][y] != -1:
            if square[x][y] in opts:
                opts = set([square[x][y]])
            else:
                return
        # FIXME __MIN__ Is the histogram really best?
        for _, opt in sorted(((hist[opt], opt) for opt in opts)):
        #for opt in opts:
            n_square = deepcopy(square)
            n_square[x][y] = opt
            n_non_symmetry_cost = _non_symmetry_cost 
            if x != y and n_square[x][y] != -1 and n_square[y][x] != -1 and n_square[x][y] != n_square[y][x]:
                n_non_symmetry_cost += 1
            # TODO: Cut short from here if too large...
            n_hist = Counter(hist)
            n_x, n_y = x + 1, y
            if n_x == n:
                n_x = 0
                n_y += 1
            # new set of primes
            n_set_of_primes = set(set_of_primes)
            n_primes = set()
            if 30 <= index <= 35:
                v = [n_square[index % 6][j] for j in range(6)]
                p = int(''.join(map(str, v)))
                n_primes.add(p)
            if index % 6 == 5:
                v = [n_square[i][index // 6] for i in range(6)] 
                p = int(''.join(map(str, v)))
                n_primes.add(p)
            if index == 30:
                v = [n_square[i][n-i-1] for i in range(n)]
                p = int(''.join(map(str, v)))
                n_primes.add(p)
            if index == 35:
                v = [n_square[i][i] for i in range(n)]
                p = int(''.join(map(str, v)))
                n_primes.add(p)
            for si in n_primes:
                if si in n_set_of_primes:
                    continue
                n_set_of_primes.add(si)
                for sii in map(int, list(str(si))):
                    n_hist[sii] += 1
            _cost = 0
            for _, v in n_hist.items():
                _cost += (v*(v-1)) // 2
            fill(n_square, (n_x, n_y), n_hist, index + 1, n_set_of_primes, _cost, n_non_symmetry_cost)

    trie = PrimesTrie(primes)
    #for p in primes:
    # for p in [517823]:
    #     p = list(map(int, str(p)))
    #     m = [[-1 for i in range(n)] for j in range(n)]
    #     m[0][0] = p[0]
        
    #     m[0][1] = p[1]
    #     m[0][2] = p[2]
    #     m[0][3] = p[3]
    #     m[0][4] = p[4]
    #     m[0][5] = p[5]

    #     m[1][0] = p[1]
    #     m[2][0] = p[2]
    #     m[3][0] = p[3]
    #     m[4][0] = p[4]
    #     m[5][0] = p[5]

    #     m[1][1] = p[1]
    #     m[2][2] = p[2]
    #     m[3][3] = p[3]
    #     m[4][4] = p[4]
    #     m[5][5] = p[5]
    # m = [[5, 1, 7, 8, 2, 3], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1]]
    # fill(m, (0, 0), Counter(), 0, set(), 0, 0)
    fill([[-1 for i in range(n)] for j in range(n)], (0, 0), Counter(), 0, set(), 0, 0)


def solve(n):
    # For each value of a in increasing order, find the squares with primes
    H = defaultdict(list)
    for p in range(10**(n-1), 10**n):
        if isprime(p):
            A = sum(map(int, list(str(p))))
            if A % 2 == 1:
                # for n == 6, the sum of the last line of the matrix is always
                #  even, as the terms are in {1, 3, 7, 9}. 
                # So we can skip the odd sums.
                continue
            H[A] += [p]
    # FIXME
    # for a in sorted(H.keys()):
    #     print(a, len(H[a]))
    # exit(0)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        todo = ((n, a, H[a]) for a in sorted(H.keys()))
        for res in executor.map(solve_parallel, todo):
            pass


if __name__ == "__main__":
    solve(6)
