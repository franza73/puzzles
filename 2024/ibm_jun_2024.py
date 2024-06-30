
'''
  We can use the equivalent representation (for m > n) for the pitagorean
triples:
  a = m**2 - n**2
  b = 2*m*n
  c = m**2 + n**2
and the problem specifies a/b = pi.
  So our problem now is to find a fractional x (i.e. m/n) that solves the
equation x/2 + 0.5/x = pi, with the correct precision. We solve the
equation by applying the Stern-Brocott method.
'''
from math import gcd
from mpmath import mp


def approx(val, delta):
    '''
    Use Stern-Brocott approximation to solve the equation.
    '''
    a_n, a_d = mp.mpf('0'), mp.mpf('1')
    b_n, b_d = mp.mpf('1'), mp.mpf('0')
    while True:
        m, n = a_n+b_n, a_d+b_d
        x = m/n
        fx = x/2 - 1/(2*x)
        if fx < val:
            a_n, a_d = m, n
        elif fx > val:
            b_n, b_d = m, n
        eps = mp.fabs(fx - val)
        if eps < mp.mpf('10')**(-delta):
            m, n = int(m), int(n)
            a = m**2 - n**2
            b = 2*m*n
            c = m**2 + n**2
            assert a**2 + b**2 == c**2
            g = gcd(a, b, c)
            return a//g, b//g, c//g


if __name__ == "__main__":
    mp.dps = 300

    A, B, C = approx(mp.pi, 20)
    print(f'With max number of digits {len(str(C))}:')
    print(f'A = {A}\nB = {B}\nC = {C}\neps = ', end='')
    mp.nprint(mp.fabs(mp.mpf(A)/mp.mpf(B) - mp.pi), 3)

    D, E, F = approx(mp.pi, 95)
    print(f'With max number of digits {len(str(F))}:')
    print(f'D = {D}\nE = {E}\nF = {F}\neps = ', end='')
    mp.nprint(mp.fabs(mp.mpf(D)/mp.mpf(E) - mp.pi), 3)
