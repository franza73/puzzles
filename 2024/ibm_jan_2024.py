'''
Fill the square with nine positions at the top left side ('a' to 'i' in the
diagram bellow). Do this three by three, as (a, b, c) defines j, (d, e, f)
define k and (g, h, i) define l. Remaining 'm' to 'p' can at this point also
be obtained similarly.
This way, we can calculate the values at the missing positions ('j' to 'p',
on this order) based on the expected horizontal and vertical totals.

a  b  c  j -- e1
d  e  f  k -- e2
g  h  i  l -- e3
m  n  o  p -- e8
|  |  |  |
e4 e5 e6 e7

(extra credit)
Iterate through all pairs of solutions to the original problem, while trying
all the options of +/- signals between these numbers.
The numbers can be taken four by four, and next iterations are explored only
when the previous partial results match.
'''
from itertools import permutations, combinations


def eqn(val, ops, index):
    '''
    evaluates the equation with index equal to 'index'
    0 -> 3 horizontal (top to down)
    4 -> 7 vertical (left to right)
    '''
    res = 0
    if index < 4:
        for v_i, o_i in zip(val[index*4:index*4+4], [1]+ops[index*3:index*3+3]):
            res += v_i*o_i
    else:
        for v_i, o_i in zip(val[index-4::4], [1]+ops[index*3:index*3+3]):
            res += v_i*o_i
    return res


def triple(val):
    '''
    help to create triples of signals to be used to explore the equations
    '''
    return 1 if val & 4 else -1, 1 if val & 2 else -1, 1 if val & 1 else -1


def signs(arg):
    '''
    pretty print the signs in the format specified by the problem
    '''
    res_s = []
    res = [[] for _ in range(7)]
    for index in range(4):
        res[2*index] = arg[index*3:index*3+3]
    for index in range(3):
        res[2*index+1] = arg[index+12::3]
    for r_i in res:
        for r_i_i in r_i:
            res_s += ['+' if r_i_i == 1 else '-']
    return '[' + ','.join(res_s) + ']'


# Loops through options
sols = []
A = set(range(1, 17))
for a, b, c in permutations(A, 3):
    # e1
    j = a + b - c - 5
    if not 1 <= j <= 16:
        continue
    if len(set([a, b, c, j])) != 4:
        continue
    B = A.difference(set([a, b, c, j]))
    for d, e, f in permutations(B, 3):
        # e2
        k = d + e + f - 10
        if not 1 <= k <= 16:
            continue
        if len(set([a, b, c, d, e, f, j, k])) != 8:
            continue
        C = B.difference(set([d, e, f, k]))
        for g, h, i in permutations(C, 3):
            # e3
            l = 9 - (g - h + i)
            if not 1 <= l <= 16:
                continue
            if len(set([a, b, c, d, e, f, g, h, i, j, k, l])) != 12:
                continue
            # e4
            m = (a + d + g) - 17
            if not 1 <= m <= 16:
                continue
            if len(set([a, b, c, d, e, f, g, h, i, j, k, l, m])) != 13:
                continue
            # e5
            n = (b + e - h) - 8
            if not 1 <= n <= 16:
                continue
            if len(set([a, b, c, d, e, f, g, h, i, j, k, l, m, n])) != 14:
                continue
            # e6
            o = 11 - (c - f - i)
            if not 1 <= o <= 16:
                continue
            if len(set([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o])) != 15:
                continue
            # e7
            p = 48 - (j + k + l)
            if not 1 <= p <= 16:
                continue
            # e8
            if m - n + o - p != 0:
                continue
            if len(set([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p])) != 16:
                continue
            sols.append([a, b, c, j, d, e, f, k, g, h, i, l, m, n, o, p])

print(f'There are {len(sols)} solutions. One of them is {sols[0]}')

# Extra credit
OPS = [1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1, 1]
assert signs(OPS) == '[+,-,-,+,+,-,+,+,+,-,+,-,-,+,-,+,+,-,-,+,+,-,+,-]'

print('Solutions to the extra credit:')
for p_0, p_1 in combinations(sols, 2):
    for p_0_i, p_1_i, in zip(p_0, p_1):
        if p_0_i == p_1_i:
            break
    else:
        for a in range(8):
            ops_a = list(triple(a))
            if eqn(p_0, ops_a, 0) != eqn(p_1, ops_a, 0):
                continue
            for b in range(8):
                ops_b = list(ops_a) + list(triple(b))
                if eqn(p_0, ops_b, 1) != eqn(p_1, ops_b, 1):
                    continue
                for c in range(8):
                    ops_c = list(ops_b) + list(triple(c))
                    if eqn(p_0, ops_c, 2) != eqn(p_1, ops_c, 2):
                        continue
                    for d in range(8):
                        ops_d = list(ops_c) + list(triple(d))
                        if eqn(p_0, ops_d, 3) != eqn(p_1, ops_d, 3):
                            continue
                        for e in range(8):
                            ops_e = list(ops_d) + list(triple(e))
                            if eqn(p_0, ops_e, 4) != eqn(p_1, ops_e, 4):
                                continue
                            for f in range(8):
                                ops_f = list(ops_e) + list(triple(f))
                                if eqn(p_0, ops_f, 5) != eqn(p_1, ops_f, 5):
                                    continue
                                for g in range(8):
                                    ops_g = list(ops_f) + list(triple(g))
                                    if eqn(p_0, ops_g, 6) != eqn(p_1, ops_g, 6):
                                        continue
                                    for h in range(8):
                                        ops_h = list(ops_g) + list(triple(h))
                                        if eqn(p_0, ops_h, 7) != eqn(p_1, ops_h, 7):
                                            continue
                                        cnt = sum(i != j for i, j in zip(ops_h, OPS))
                                        if cnt >= 12:
                                            print()
                                            print(p_0)
                                            print(p_1)
                                            print(signs(ops_h))
