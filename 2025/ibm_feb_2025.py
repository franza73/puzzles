'''
 1061 primes for N = 4
 8363 primes for N = 5 
68906 primes for N = 6
'''
from sympy import isprime
from collections import defaultdict


N = 4
H = defaultdict(list)
for p in range(10**(N-1), 10**N):
    if isprime(p):
        A = sum(map(int, list(str(p))))
        H[A] += [p]
for a in sorted(H.keys()):
    l_a = len(H[a])
    print('A =', a, ':', l_a)

exit(0)
ms = '''5 7 9 1
1 7 7 7
7 5 3 7
9 3 3 7'''
# ms = '''1 7 7 7
# 5 5 5 7
# 9 3 9 1
# 7 7 1 7'''

# TODO _str_to_matrix
m = []
for mi in ms.splitlines():
    m += [list(map(int, mi.split()))]
print(m)

# TODO _cost
N = 4
hor = [0] * N
ver = [0] * N
diag = [0] * 2
for i in range(N):
    diag[0] = diag[0] * 10 + m[i][i]
    diag[1] = diag[1] * 10 + m[i][N-i-1]
    for j in range(N):
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
print(cost)