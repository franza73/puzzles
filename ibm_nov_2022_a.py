'''
IBM Ponder This - November 2022
'''
from sympy.solvers.diophantine.diophantine import diop_DN
from operator import itemgetter
from fractions import Fraction


V = 974170
print(diop_DN(V, 1))
print(diop_DN(V, -V+1))
SOL = []
x0, y0 = diop_DN(V, 1).pop()
for xn, yn in diop_DN(V, -V+1):
    b, a = (xn+1)//2, (yn+1)//2
    while True:
        xn, yn = (x0*xn+y0*yn*V, x0*yn+y0*xn)
        b, a = (xn+1)//2, (yn+1)//2
        if len(str(b)) >= 100:
            if b > 1:
                SOL += [(a, b)]
            break
SOL.sort(key=itemgetter(1))
a, b = SOL[0]
print(a, b)
print(Fraction(a*(a-1), b*(b-1)))