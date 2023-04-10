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
    #global best
    best = float('inf')
    best_p = 0
    for p in allPrimes:
        v = E(p, float('inf'))
        if p == 17923:
           print('*', v/len(allPrimes)) 
        if v < best:
            best = v
            best_p = p
            print(best_p, best/len(allPrimes))


if __name__ == "__main__":
    
    # -- all primes in range --
    N = 5
    allPrimes = list(sieve.primerange(10**(N-1), 10**N - 1))
    shuffle(allPrimes)

    M = 200
    cnt = 0
    allPrimesIter = allPrimes[:]
    allPrimesOriginal = allPrimes[:] 
    precalculations()
    for i in range(len(allPrimesIter)//M + 1):
        print(f'\niter {i}')
        allPrimes = allPrimesIter[0:M]
        cnt += len(allPrimes)
        best_E()
        #print(17923, E(17923, float('inf'))/len(allPrimes))
        allPrimesIter = allPrimesIter[M:]
    print(cnt, len(allPrimesOriginal))

'''
~  (⎈ |arn:aws:eks:us-west-2:438164822453:cluster/gjp-v1:default)
▶ time /usr/local/bin/python3 ibm_mar_2022_small.py
15569 266.7670692335286
76231 129.13703216549087
72493 128.39591055841206
39827 127.2104507951692
19753 122.90051416955637
13729 122.14647853641038
12973 121.76742795647495
17293 121.61939495396389
17923 121.5416716489298
/usr/local/bin/python3 /Users/franciraldocavalcante/ibm_mar_2022_small.py
8610.98s user 45.87s system 97% cpu 2:27:23.97 total
=>
2.5 hours
'''
