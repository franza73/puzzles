'''
IBM Ponder This - November 2022
'''
from sympy.solvers.diophantine.diophantine import diop_DN
from math import sqrt
from fractions import Fraction


for V in range(2, 616):
    if int(sqrt(V))**2 == V:
        continue
    x0, y0 = diop_DN(V, 1).pop()
    SOL = set()
    for xn, yn in diop_DN(V, -V+1):
        if len(SOL) > 16:
            break
        b, a = (xn+1)//2, (yn+1)//2
        if b > 1 and len(str(b)) < 100:
            SOL.add((a, b))
        elif len(str(b)) >= 100:
            break
        while True:
            if len(SOL) > 16: 
                break
            xn, yn = (x0*xn+y0*yn*V, x0*yn+y0*xn)
            b, a = (xn+1)//2, (yn+1)//2
            if b > 1 and len(str(b)) < 100:
                SOL.add((a, b))
            elif len(str(b)) >= 100:
                break
    if len(SOL) == 16:
        print(f'D = {V} has exactly 16 solutions (a, b) with length of b less than 100:')
        SOL = list(SOL)
        SOL.sort()
        for a, b in SOL:
            print(len(str(b)), (a, b), Fraction(a*(a-1), b*(b-1)))
        break
