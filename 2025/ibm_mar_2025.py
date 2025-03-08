import numpy as np
from fractions import Fraction
from collections import defaultdict
from random import randrange


def to_fraction(x):
    return Fraction(x).limit_denominator()

def effective_resistance(i, j, L_pinv):
    return L_pinv[i, i] + L_pinv[j, j] - 2 * L_pinv[i, j]

def create_a(pos, n):
    a = np.zeros([n, n])
    H = defaultdict(set)
    for x, y in pos:
        H[x-1].add(y-1)
        H[y-1].add(x-1)
        a[x-1, y-1] += 1
        a[y-1, x-1] += 1
    return a, all(len(H[a]) > 1 for a in range(n))

def score(n, A):
    D = np.diag(np.sum(A, axis=1))
    L = D - A
    L_pinv = np.linalg.pinv(L)
    values = set()
    for i in range(n):
        for j in range(n):
            if i >= j:
                continue
            r = effective_resistance(i, j, L_pinv)
            #print(f"R[{i+1},{j+1}] =", to_fraction(r))
            values.add(to_fraction(r))
    #print(len(values), values)
    return len(values) if '0' not in values else -1


# edges = [(1, 6), (1,4), (2,5), (2,6), (3,5), (3,5), (3,6), (4,5), (4,5)]
# a, is_valid = create_a(edges, 6)
# print(score(5, a))
# print(is_valid)
# exit(0)
# A = np.array([
#     [0, 1, 0, 1],
#     [1, 0, 2, 0],
#     [0, 2, 0, 1],
#     [1, 0, 1, 0]
# ], dtype=float)
# print(score(3, A))

# A = np.array([
#     [0, 1, 0, 0, 1],
#     [1, 0, 2, 0, 0],
#     [0, 2, 0, 1, 1],
#     [0, 0, 1, 0, 1], 
#     [1, 0, 1, 1, 0]
# ], dtype=float)

# A = np.array([
#     [0, 1, 0, 0, 1, 1],
#     [1, 0, 2, 0, 0, 0],
#     [0, 2, 0, 1, 0, 0],
#     [0, 0, 1, 0, 1, 0], 
#     [1, 0, 0, 1, 0, 1],     
#     [1, 0, 0, 0, 1, 0]
# ], dtype=float)
# print(score(4, A))
# exit(0)
# A = np.array([
#     [0, 0, 0, 1, 0, 1],
#     [0, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 2, 1],
#     [1, 0, 0, 0, 2, 0],
#     [0, 1, 2, 2, 0, 0],
#     [1, 1, 1, 0, 0, 0]
# ], dtype=float)
# Asum = A.sum() // 2
# print(score(5, A))
# print(A)
n = [(i, j) for i in range(1, 6) for j in range(1, 6) if j > i]
lst = [n[randrange(0, len(n))] for _ in range(8)]
while True:
    index = randrange(0, len(n))
    lst_pos = randrange(0, 8)
    a, is_valid = create_a(lst, 5)
    if not is_valid:
        lst[lst_pos] = n[index] 
        continue
    prev_score = score(5, a)
    if prev_score == 10: 
        print(a, prev_score, lst)
        break
    lst[lst_pos] = n[index]