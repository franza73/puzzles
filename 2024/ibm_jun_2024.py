# ---------------------------------------------------------------------------
# We can use the equivalent representation (for m > n) for the pitagorean
# triples:
# a = m**2 - n**2
# b = 2*m*n
# c = m**2 + n**2
# and the problem specifies a/b = pi.
# So our problem now is to find a fractional x (i.e. m/n) that solves the
# equation x/2 + 0.5/x = pi, with the correct precision. We solve the
# equation by applying the Stern-Brocott method.
# ---------------------------------------------------------------------------
from mpmath import mp
from math import gcd


def approx(val, delta):
    a, b = mp.mpf('0'), mp.mpf('1')
    c, d = mp.mpf('1'), mp.mpf('0')
    while True:
        m, n = a+c, b+d
        x = m/n
        fx = x/mp.mpf('2.0') - mp.mpf('0.5')/x
        if fx < val:
            a, b = m, n
        elif fx > val:
            c, d = m, n
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

    a, b, c = approx(mp.pi, 20)
    print(f'With max number of digits {len(str(c))}:')
    print(f'A = {a}\nB = {b}\nC = {c}\neps = ', end='')
    mp.nprint(mp.fabs(mp.mpf(a)/mp.mpf(b) - mp.pi), 3)

    d, e, f = approx(mp.pi, 95)
    print(f'With max number of digits {len(str(f))}:')
    print(f'D = {d}\nE = {e}\nF = {f}\neps = ', end='')
    mp.nprint(mp.fabs(mp.mpf(d)/mp.mpf(e) - mp.pi), 3)
