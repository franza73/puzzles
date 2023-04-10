from math import log


def solve(n):
    if n in H:
        return H[n]
    I, J, n0 = 0, 0, n
    while n % 2 == 0:
        n //= 2
        I += 1
    while n % 3 == 0:
        n //= 3
        J += 1
    if n == 1:
        H[n0] = [(I, J)]
        return H[n0]
    elif n0 != n:
        H[n0] = list(map(lambda x: (x[0]+I, x[1]+J), solve(n)))
        return H[n0]
    p = int(log(n)/log(2))
    if 2**p % 3 != n % 3:
        p -= 1
    best = float('inf')
    best_v = []
    for i in range(p, max(0, p-4), -2):
        n1 = n - 2**i
        k = 0
        while n1 % 3 == 0:
            n1 //= 3
            k += 1

        d_v = list(map(lambda x: (x[0], x[1]+k), solve(n1)))
        if len(d_v) == 0:
            next
        if not (d_v[0][0] > i and d_v[0][1] < 0):
            next
        v = [(i, 0)] + d_v

        if best > len(v):
            best = len(v)
            best_v = v

    H[n0] = best_v[:]
    return H[n0]


H = {}
res = 0
N = 10**199
#N = 10100100101110110000
l = solve(N)
x_1, y_1 = 0, 0
for x, y in l:
    res += (2**x)*(3**y)
    if x_1 != 0 and y_1 != 0:
        print(x, x_1, y, y_1)
        assert(x < x_1 and y > y_1)
    x_1, y_1 = x, y
print(N)
print(res, len(l), l)
