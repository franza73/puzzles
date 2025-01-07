'''
Solution:
39 TC CA TC CA AS CA TC CA TC AB CA TC CA AS CA TC CA AS CA TC CA TC CA
   AS CA TC CA TC CA AS CA TC CA AS CA TC CA TC CA
In 258.62s

Solution to the bonus question:
11 TA AB AC TA AC CS AC CS AC TA AC
Vc = 4224/3187
In additional 113.13s
'''
from math import sqrt
from collections import deque


def solve(va, vb, vc, eps):
    def neigh(state):
        a, b, c = state
        res = []
        if a < va:
            res += [('TA', (va, b, c))]
        if b < vb:
            res += [('TB', (a, vb, c))]
        if c < vc:
            res += [('TC', (a, b, vc))]
        if a != 0:
            res += [('AS', (0, b, c))]
            if a + b <= vb:
                res += [('AB', (0, a + b, c))]
            else:
                res += [('AB', (a + b - vb, vb, c))]
            if a + c <= vc:
                res += [('AC', (0, b, a + c))]
            else:
                res += [('AC', (a + c - vc, b, vc))]
        if b != 0:
            res += [('BS', (a, 0, c))]
            if a + b <= va:
                res += [('BA', (a + b, 0, c))]
            else:
                res += [('BA', (va, a + b - va, c))]
            if b + c <= vc:
                res += [('BC', (a, 0, b + c))]
            else:
                res += [('BC', (a, b + c - vc, vc))]
        if c != 0:
            res += [('CS', (a, b, 0))]
            if a + c <= va:
                res += [('CA', (a + c, b, 0))]
            else:
                res += [('CA', (va, b, a + c - va))]
            if b + c <= vb:
                res += [('CB', (a, b + c, 0))]
            else:
                res += [('CB', (a, vb, b + c - vb))]
        return res

    todo = deque([(0, (0, 0, 0))])
    visited = set()
    prev = {}
    sol = ()
    while todo:
        depth, state = todo.popleft()
        if state in visited:
            continue
        a, b, c = state
        if min(abs(a - 1), abs(b - 1), abs(c - 1)) < eps:
            sol = state
            break
        visited.add(state)
        for move, n in neigh(state):
            if n in visited:
                continue
            if n not in prev:
                prev[n] = [move, state]
            todo += [(depth+1, n)]
    res = []
    while sol in prev:
        res.append(prev[sol][0])
        sol = prev[sol][1]
    return len(res), ' '.join(res[::-1])

def approx(i, j, k, val, delta):
    a_n, a_d = 0, 1
    b_n, b_d = 1, 0
    while True:
        m, n = a_n+b_n, a_d+b_d
        x = m/n
        fx = i*sqrt(5) + j*sqrt(3) + k*x
        if k > 0:
            if fx < val:
                a_n, a_d = m, n
            elif fx > val:
                b_n, b_d = m, n
        else:
            if fx > val:
                a_n, a_d = m, n
            elif fx < val:
                b_n, b_d = m, n            
        eps = abs(fx - val)
        if eps < 10**(-delta):
            m, n = int(m), int(n)
            return m, n
        
if __name__ == "__main__":
    va, vb, vc = sqrt(5), sqrt(3), sqrt(2)
    print('Reproduce the example:')
    print(solve(va, vb, vc, 0.01))
    print('Solution:')
    print(solve(va, vb, vc, 0.0003))
    print('Bonus question:')
    for i in range(-10, 11):
        for j in range(-10, 11):
            for k in range(-10, 11):
                if k == 0: continue
                vc = (1 - i*sqrt(5) - j*sqrt(3)) / k
                m = abs(i) + abs(j) + abs(k)
                if vc < 0 or vc > sqrt(3) or m > 11:
                    continue
                if solve(va, vb, vc, 10**(-8))[0] == 11:
                    vc_n, vc_d = approx(i, j, k, 1, 8) 
                    print(i, j, k, (vc_n, vc_d))
                    print(solve(va, vb, vc_n/vc_d, 10**(-8)))
                    print('---------')
