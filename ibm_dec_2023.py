#!/usr/bin/env python3
'''
Finds Eisenstein Integers (see Wikipedia) with specified norm range.

Result:
4310930 1000000
4311298 1000000
4312919 1000000
4313134 1000000
4313718 1000000
'''


for N in range(4310000, 4314000):
    H = set()
    y0 = N
    N2 = N**2
    N1_2 = (N+1)**2
    for x in range(N+1):
        for y in range(y0, x-1, -1):
            v = x**2 + x*y + y**2
            if N2 < v < N1_2:
                H.add(v)
                y0 = y
            elif v <= N2:
                break
    if len(H) == 1000000:
        print(N, len(H))
