import re
from math import log
from collections import defaultdict


def solve(N, budget):
    def prepare_hash():
        maximum = int('1'*N)
        max1 = int(log(maximum)/log(2)) + 1
        max2 = int(log(maximum)/log(3)) + 1
        _hash = defaultdict(list)
        for a in range(max1):
            for b in range(max2):
                v = (2**a)*(3**b)
                if v > maximum:
                    break
                _hash[len(str(v))] += [(v, a, b)]
        return _hash
    mem = prepare_hash()
    total = 0
    result = []
    best_len, best_v, best_a, best_b = 0, 0, 0, 0
    while best_len < N:
        for h, a, b in mem[N - best_len]:
            m = re.search(r'^(1[01]*0)', str(total + h))
            if m:
                v = m.span()[1]
                if v > best_len:
                    best_len, best_v, best_a, best_b = v, h, a, b
        total += best_v
        result += [(best_a, best_b)]
    assert len(str(total)) == N
    assert len(result) < budget
    return total, result

total, result = solve(200, 150)
print('N = 200, length =', len(result))
print(total)
print(result)

total, result = solve(300, 215)
print('N = 300, length =', len(result))
print(total)
print(result)
