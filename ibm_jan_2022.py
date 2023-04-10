'''
IBM Ponder this Jan 2022

-- small --
[9, 4, 5, 2, 1, 7, 3] 3051
[8, 5, 4, 1, 0, 6, 2] 446

-- large --
[9, 7, 6, 4, 3, 2, 8, 1] 23209
[9, 6, 0, 1, 4, 8, 2, 5] 8265
'''
from collections import defaultdict
from itertools import permutations, combinations
from sympy import sieve


def score(value, primes):
    '''
    Calculate the score of a permutation
    '''
    total = 0
    for p_i in primes:
        prev = None
        for c_i in map(int, list(str(p_i))):
            if prev is not None:
                d_i = abs(value.index(c_i) - prev)
                total += min(d_i, n - d_i)
            prev = value.index(c_i)
    return total


n, d = 7, 5
# n, d = 8, 6
# numbers that follow the criteria:
N = defaultdict(set)
for i in sieve.primerange(10**(d-1), 10**d):
    si = set(str(i))
    if len(si) == d:
        N[''.join(sorted(si))].add(i)

vmin, vmax = float("inf"), 0
lmin, lmax = None, None
for s in combinations(range(10), n):
    V = set()
    for si in combinations(s, d):
        V.update(N[''.join(map(str, sorted(si)))])
    M = max(s)
    for si in permutations(s):
        lst = list(si)
        if lst[0] == M and lst[1] > lst[-1]:
            # takes care of circular list duplicates:
            # 1. first item is the larger
            # 2. second item is always larger than last
            # FIXME There's a better way to do these circular_permutations
            last_score = score(lst, V)
            if last_score < vmin:
                vmin = last_score
                lmin = lst
            if last_score > vmax:
                vmax = last_score
                lmax = lst
print(lmax, vmax)
print(lmin, vmin)
