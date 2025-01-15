'''
Solution:
39 TC CA TC CA AS CA TC CA TC AB CA TC CA AS CA TC CA AS CA TC CA TC CA
   AS CA TC CA TC CA AS CA TC CA AS CA TC CA TC CA

Solution to the bonus question:
11 TA AB AC TA AC CS AC CS AC TA AC
Vc = 4224/3187
'''
from math import sqrt
from collections import deque


class Jug:
    ''' Jug class that can be used to simulate the state of the problem '''
    def __init__(self, v0, v1, v2, _vc):
        self.v = (v0, v1, v2)
        self.vc = _vc

    def __add__(self, other):
        return Jug(self.v[0] + other.v[0], self.v[1] + other.v[1],
                   self.v[2] + other.v[2], self.vc)

    def __sub__(self, other):
        return Jug(self.v[0] - other.v[0],
                   self.v[1] - other.v[1], self.v[2] - other.v[2], self.vc)

    def __str__(self):
        return str(self.v)

    def eval(self):
        ''' Numerical value for the jug content '''
        return self.v[0]*sqrt(5) + self.v[1]*sqrt(3) + self.v[2]*self.vc

    def __lt__(self, other):
        if self.eval() < other.eval():
            return True
        return False

    def __ne__(self, other):
        if isinstance(other, int):
            return self.eval() != other
        return self.eval() == other.eval()

    def __eq__(self, other):
        return self.eval() == other.eval()

    def __hash__(self):
        return hash(self.v)


def _reconstruct_path(sol, prev):
    res = []
    while sol in prev:
        res.append(prev[sol][0])
        sol = prev[sol][1]
    return len(res), ' '.join(res[::-1])


def _min_dist_to_one(state):
    a, b, c = state
    return min(abs(a.eval() - 1), abs(b.eval() - 1), abs(c.eval() - 1))


def solve(_vc, eps):
    ''' Solve the problem with specified precision '''
    def _neigh(state):
        a, b, c = state
        res = []
        if a < va:
            res += [('TA', (va, b, c))]
        if b < vb:
            res += [('TB', (a, vb, c))]
        if c < vc:
            res += [('TC', (a, b, vc))]
        if a != 0:
            res += [('AS', (z, b, c))]
            res += [('AB', (max(z, a + b - vb), min(a + b, vb), c))]
            res += [('AC', (max(z, a + c - vc), b, min(a + c, vc)))]
        if b != 0:
            res += [('BS', (a, z, c))]
            res += [('BA', (min(a + b, va), max(z, a + b - va), c))]
            res += [('BC', (a, max(z, b + c - vc), min(b + c, vc)))]
        if c != 0:
            res += [('CS', (a, b, z))]
            res += [('CA', (min(a + c, va), b, max(z, a + c - va)))]
            res += [('CB', (a, min(b + c, vb), max(z, b + c - vb)))]
        return res

    va = Jug(1, 0, 0, _vc)
    vb = Jug(0, 1, 0, _vc)
    vc = Jug(0, 0, 1, _vc)
    z = Jug(0, 0, 0, _vc)
    todo = deque([(0, (z, z, z))])
    visited = set()
    prev = {}
    sol = ()
    while todo:
        depth, state = todo.popleft()
        if state in visited:
            continue
        if _min_dist_to_one(state) < eps:
            sol = state
            break
        visited.add(state)
        for move, n in _neigh(state):
            if n in visited:
                continue
            if n not in prev:
                prev[n] = [move, state]
            todo += [(depth+1, n)]
    return _reconstruct_path(sol, prev)


def approx(i, j, k, val, eps):
    ''' Approximation to find fractional vc '''
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
        if abs(fx - val) < eps:
            m, n = int(m), int(n)
            return m, n


def main():
    ''' Solve both parts of the problem '''
    print('Reproduce the example:')
    print(solve(sqrt(2), 0.01))

    print('Solution:')
    print(solve(sqrt(2), 0.0003))

    print('Bonus question:')
    eps = 10**(-8)
    for i in range(-10, 11):
        for j in range(-10, 11):
            for k in range(-10, 11):
                if k == 0:
                    continue
                vc = (1 - i*sqrt(5) - j*sqrt(3)) / k
                m = abs(i) + abs(j) + abs(k)
                if vc < 0 or vc > sqrt(3) or m > 11:
                    continue
                if solve(vc, eps)[0] == 11:
                    vc_n, vc_d = approx(i, j, k, 1, eps)
                    print(i, j, k, (vc_n, vc_d))
                    print(solve(vc_n/vc_d, eps))
                    print('---------')


if __name__ == "__main__":
    main()
