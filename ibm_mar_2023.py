from sympy import isprime


class Solve:
    best = 0
    N = 5
    T = 4.0

    def dig(self, p0, n):
        if n > self.N or (n > 1 and len(str(p0)) / n < self.T):
            return
        elif n == self.N and p0 > self.best:
            self.best = p0
        for pi in range(10):
            p = 10 * p0 + pi
            if isprime(p):
                self.dig(p, n)
            else:
                self.dig(p, n + 1)
        return self.best

    def solve(self):
        res = 0
        for p in range(1, 10):
            res = max(res, self.dig(p, 0 if isprime(p) else 1))
        return res


class SolveStar:
    best = 0
    N = 5
    T = 8.2

    def dig(self, p0, n, d):
        if n > self.N or (n > 1 and d / n < self.T):
            return
        elif n == self.N and p0 > self.best:
            self.best = p0
        for pi in range(1, 10):
            p = pi * 10**d + p0
            if isprime(p):
                self.dig(p, n, d + 1)
            else:
                self.dig(p, n + 1, d + 1)
        return self.best

    def solve(self):
        res = 0
        for p in range(1, 10):
            res = max(res, self.dig(p, 0 if isprime(p) else 1, 1))
        return res


# 3733799911799539139382193991 is the result of the 1st part
print('best:\t', Solve().solve())

# 996381323136248319687995918918997653319693967 is the 2nd result
print('best *:\t', SolveStar().solve())
