from collections import defaultdict
from random import shuffle
from sympy import sieve
from heapq import heappush, heappop


def f(p, q):
    def intersect(pars):
        assert(len(pars) > 0)
        result = pars[0]
        for i in range(1, len(pars)):
            result = result.intersection(pars[i])
        return result

    S = set(map(int, str(q)))
    res = []
    i = 0
    for pi, qi in zip(map(int, list(str(p))), map(int, list(str(q)))):
        if pi == qi:
            res += [GREEN[pi, i]]
        elif pi in S:
            res += [YELLOW[pi, i]]
        else:
            res += [GRAY[pi]]
        i += 1
    return len(intersect(res))


def E(p):
    res = 0
    for q in allPrimes:
        res += f(p, q)
    return res


def precalculations():
    global GREEN, YELLOW, GRAY
    GREEN = defaultdict(set)
    YELLOW = defaultdict(set)
    GRAY = defaultdict(set)

    for p in allPrimes:
        for i, pi in enumerate(map(int, list(str(p)))):
            GREEN[pi, i].add(p)
        for pi in set(range(10)) - set(map(int, list(str(p)))):
            GRAY[pi].add(p)
    for i in range(10):
        CONTAINS = set()
        for j in range(N):
            CONTAINS = CONTAINS.union(GREEN[i, j])
        for j in range(N):
            YELLOW[i, j] = CONTAINS - GREEN[i, j]


def best_E():
    q = []
    L = len(allPrimes)
    #for p in sorted(sorted(allPrimesOriginal), key=lambda x: len(set(list(str(x)))), reverse=True):
    for p in sorted(list(filter(lambda x: len(set(list(str(x)))) == N, allPrimesOriginal))):
        v = E(p)
        heappush(q, (v/L, p))
        #print(q[0], p)
        #print( (v/L, p) )
    while q:
        print(heappop(q))


if __name__ == "__main__":
    # -- all primes in range --
    N = 7
    allPrimes = list(sieve.primerange(10**(N-1), 10**N - 1))
    shuffle(allPrimes)

    M = 10
    allPrimesOriginal = allPrimes[:]
    precalculations()
    
    allPrimes = allPrimesOriginal[0:M]
    best_E()

    '''
    >>> some = list(filter(lambda x: len(set(list(str(x))))==N, allPrimes))
    >>> len(some)
    33950

    (1113.08,  5102437)
    (1118.5, 1075843)
    (1122.22,  2745031)
    (1154.445, 4620397)
    (1155.255, 5420963)
    (1167.455, 5062489)
    '''
