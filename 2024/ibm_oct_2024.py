''' IBM Ponder This October 2024

We start with the smaller option for B (1*2*3*4*6*7*8*9), then multiply
it by the valid digits, that implies in composed increments by {2, 3, 7}
that can generate all larger values of B.

We use a min heap for this process of growing B, creating the B values in
increasing order.

The process generates pairs (B, X_factors). From these we can calculate
A_factors as the terms of the digit product on X that are not in the digit
product of B.

And A can be obtained from a_factors by recursion. Here is the rationale:

    A * 10**k + B = M * B
    A * 10**k = (M-1) * B = N * B

but 5 cannot divide B (would be a contradiction with the problem's
assumptions), so,

   A * 2**k   = Q * B, with Q = N // 5**k
   A = R * (B // 2**min(k, k2))

   where k2 is the exponent of 2 on B (B = 2**k2 * 3**k3 * 7**k7).

   And R = Q // max(0, k - k2).

   The equation for A can be used as a recursion:

   A[0] = 0
   A[n] = A[n-1] + (B // 2**min(k, k2))

   and when A[n] doesn't contain {0, 5}, and all the eight digits are
used, and all it's terms are the expected values (A_factors), we have
reached a solution.

   As each different value of B defines a different recursion, then the
whole candidate is a good case for parallel calculation.

   After adjusting the value of the exponents to cut short large estimations,
we could solve the two problem in effective time.

   In summary:

   X_factors => B => B_factors => A_factors => A => X

'''
from collections import Counter
from heapq import heappop, heappush
from multiprocessing import Pool
import os


def decimal_to_factors(d):
    h = Counter({2: 0, 3: 0, 7: 0})
    for di in str(d):
        di = int(di)
        if di in h:
            h[di] += 1
        elif di == 4:
            h[2] += 2
        elif di == 9:
            h[3] += 2
        elif di == 6:
            h[2] += 1
            h[3] += 1
        elif di == 8:
            h[2] += 3
    return h


def is_free_of_0_5(_n):
    s = str(_n)
    return '0' not in s and '5' not in s


class Problem():
    def __init__(self, problem, max_exp):
        self.problem = problem
        self.max_exp = max_exp

    def _dig(self, args):
        _b, _x_factors, _a_factors = args
        k = len(str(_b))
        a0 = _b // 2**min(_x_factors[2], k)
        a = 0
        while True:
            a += a0
            if is_free_of_0_5(a):
                sz = len(str(a))+k
                if sz > self.max_exp:
                    break
                v = decimal_to_factors(a)
                _a_factors[1] = v[1]
                if v == _a_factors:
                    x = a * 10**k + _b
                    if len(set(list(str(x)))) < 8:
                        continue
                    print(f'x = {x}, a = {a}, b = {_b}, len = {sz}')
                    break

    def solve(self):
        def _b_is_square():
            for di in x_factors:
                if x_factors[di] % 2 != 0:
                    return False
            return True

        def _a_is_cube():
            for di in a_factors:
                if a_factors[di] % 3 != 0:
                    return False
            return True

        def _key(d):
            return ','.join([f'{k}:{d[k]}' for k in sorted(d.keys())])

        if self.problem == 'b_is_square':
            cond_2_3 = _b_is_square
        elif self.problem == 'a_is_cube':
            cond_2_3 = _a_is_cube
        x0_factors = Counter({2: 7, 3: 4, 7: 1})
        b0 = 1*2*3*4*6*7*8*9
        small_deltas = [(2, Counter({2: 1})),
                        (3, Counter({3: 1})),
                        (7, Counter({7: 1}))]
        visited = set()
        tasks = []
        heap = []
        heappush(heap, (b0, x0_factors))
        while heap:
            b, x_factors = heappop(heap)
            visited_key = _key(x_factors)
            if visited_key in visited:
                continue
            visited.add(visited_key)
            if is_free_of_0_5(b):
                b_factors = decimal_to_factors(b)
                if any(x_factors[ki] < b_factors[ki] for ki in [2, 3, 7]):
                    continue
                a_factors = x_factors - b_factors
                if cond_2_3():
                    tasks += [(b, x_factors, a_factors)]
            for bs, hs in small_deltas:
                b_n = b*bs
                x_factors_n = Counter(x_factors) + hs
                if b_n > 10**self.max_exp:
                    continue
                heappush(heap, (b_n, x_factors_n))
        with Pool(os.cpu_count()) as pool:
            pool.map(self._dig, tasks)


if __name__ == '__main__':
    Problem('b_is_square', 19).solve()
    Problem('a_is_cube', 22).solve()
