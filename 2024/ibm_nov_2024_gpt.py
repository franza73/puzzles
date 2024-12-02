import math
from itertools import product


def neighbors(_tuple):
    return list(product(*[(x, x+1, x+2) for x in _tuple]))

def cV2(p):
    x, y, z, c, a, b = p
    X = b**2 + c**2 - x**2
    Y = a**2 + c**2 - y**2
    Z = a**2 + b**2 - z**2
    return 4*a**2*b**2*c**2 - a**2*X**2 - b**2*Y**2 - c**2*Z**2 + X*Y*Z

def centroid_and_distances_from_sides(a, b, c):
    # Check if the sides form a valid triangle
    if a + b <= c or a + c <= b or b + c <= a:
        return "Invalid triangle sides"

    # Coordinates of vertices
    A = (0, 0)
    B = (c, 0)
    x_C = (a**2 - b**2 + c**2) / (2 * c)
    y_C = math.sqrt(a**2 - x_C**2)
    C = (x_C, y_C)

    # Centroid coordinates
    Gx = (A[0] + B[0] + C[0]) / 3
    Gy = (A[1] + B[1] + C[1]) / 3

    # Distances from centroid to each vertex
    d1 = round(math.sqrt((A[0] - Gx)**2 + (A[1] - Gy)**2))
    d2 = round(math.sqrt((B[0] - Gx)**2 + (B[1] - Gy)**2))
    d3 = round(math.sqrt((C[0] - Gx)**2 + (C[1] - Gy)**2))
    
    for n in neighbors((d1, d2, d3)):
        t = (a,b,c,*n)
        vol = cV2(t)
        if 120 < vol < 130:
            print(t, vol)
    return

def calc_f(a,b,c,d,e, goal):
    A = -b**2
    B = + a**2*b**2 - a**2*d**2 + a**2*e**2 - b**4 + b**2*c**2 + b**2*d**2 + b**2*e**2 + c**2*d**2 - c**2*e**2 
    C = -a**4*e**2 - a**2*b**2*c**2 + a**2*b**2*e**2 + a**2*c**2*d**2 + a**2*c**2*e**2 + a**2*d**2*e**2 - a**2*e**4 + b**2*c**2*d**2 - b**2*d**2*e**2 - c**4*d**2 - c**2*d**4 + c**2*d**2*e**2 - goal
    DLT = B**2 - 4*A*C
    if DLT < 0:
        return set()
    f_sq_0 = (-B + int(math.sqrt(DLT))) / (2*A)
    f_sq_1 = (-B - int(math.sqrt(DLT))) / (2*A)
    res = set()
    if f_sq_0 >= 0: 
        f0 = int(math.sqrt(f_sq_0))
        res.add(f0)
    if f_sq_1 >= 0:
        f1 = int(math.sqrt(f_sq_1))
        res.add(f1)
    return res

# -- main --
#goal = 144 * 3**2
goal = 128
N = 400 + 1
for a in range(2, N):
    print(a)
    for b in range(a, N):
        for c in range(max(b - a, b), min(N - a - b, b + a)):
            # -- parallel -- 
            for d in range(1, c):
                for e in range(c - d, a + b - d):
                    fset = calc_f(a, b, c, d, e, goal)
                    for f in fset:
                        t = (a, b, c, d, e, f)
                        vol = cV2(t)
                        if vol == goal:
                            print(vol, t)
exit(0)
N = 400
goal = 128
for a in range(2, N):
    for b in range(a, N):
        for c in range(b, N):
            # for d in range(2, N):
            #     for e in range(2, N):
            #         for f in calc_f(a, b, c, d, e, goal):
            #             vol = cV2((a, b, c, d, e, f))
            #             if 120 < vol < 130:
            #                 print((a, b, c, d, e, f), vol)
            sides = (a, b, c)
            centroid_and_distances_from_sides(*sides)
