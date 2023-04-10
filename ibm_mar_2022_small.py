from collections import defaultdict
from random import shuffle
from sympy import sieve


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


def E(p, cut):
    res = 0
    for q in allPrimes:
        res += f(p, q)
        if res > cut:
            break
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
    best = float('inf')
    best_p = 0
    for p in allPrimes:
        v = E(p, best)
        if v < best:
            best = v
            best_p = p
            print(best_p, best/nAllPrimes)


if __name__ == "__main__":
    # -- all primes in range --
    N = 4
    allPrimes = list(sieve.primerange(10**(N-1), 10**N - 1))
    nAllPrimes = len(allPrimes)
    # shuffle(allPrimes)

    precalculations()

    # -- test case 1 --
    if N == 4:
        assert(f(3637, 4733) == 11)
        assert(f(8731, 4733) == 8)

    # -- calculate E(.) and the min --
    best_E()