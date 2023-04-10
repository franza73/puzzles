from audioop import reverse
import re
from math import log
from collections import defaultdict


def solve(N, budget):
    def prepare_hash():
        maximum = int('1'*N)
        max1 = int(log(maximum)/log(2)) + 1
        max2 = int(log(maximum)/log(3)) + 1
        _hash = []
        for a in range(max1):
            for b in range(max2):
                v = (2**a)*(3**b)
                if v > maximum:
                    break
                _hash.append(v)
        return sorted(_hash, reverse=True)
    mem = prepare_hash()
    L = len(mem)
    for i in range(L):
        for j in range(i+1, L):
            s = mem[i] + mem[j]
            m = re.search(r'^(1[01]*)', str(s))
            if m:
                v = m.span()[1]
                print(v, s)

solve(200, 150)
