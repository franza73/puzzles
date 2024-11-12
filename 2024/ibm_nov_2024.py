'''
   --------------------------------------------------------------------------
0. After looking into the paper: "Tetrahedra with Integer Edges
and Integer Volume", I come out with a plan for solving the problem:
   0.1. Enumerate all Tetrahedra with sides smaller than some max
   value, solve for one of the sides (and the expected value of cV2), if
   there's an integer solution, stop, else, keep searching.
1. Show how to obtain the quadratic equations for 'f'.
   1.1. Use sympy for the equations.
2. As the paper analyses their method to find cV2 == 144*3**2 solutions,
   we can mimic heir method and validate their values (done),
   before looking for
   cV2 == 128 and cV2 == 655. So far have not found anything with M <= 100
   --------------------------------------------------------------------------
     + f**2 * (-a**4 + 2*a**2*b**2 + 2*a**2*c**2 + 4*a**2*i*j - 4*a**2*j**2
               - b**4
               + 2*b**2*c**2 - 4*b**2*i*j - c**4 - 4*c**2*i**2 + 4*c**2*i*j)
     + f    * (-2*a**4*j + 2*a**2*b**2*j + 2*a**2*c**2*i + 2*a**2*c**2*j
               + 2*a**2*i**2*j
               + 2*a**2*i*j**2 - 4*a**2*j**3 + 2*b**2*c**2*i - 2*b**2*i**2*j
               - 2*b**2*i*j**2 - 2*c**4*i - 4*c**2*i**3 + 2*c**2*i**2*j
               + 2*c**2*i*j**2)
              (- a**4*j**2 - a**2*b**2*c**2 + a**2*b**2*j**2 + a**2*c**2*i**2
               + a**2*c**2*j**2 + a**2*i**2*j**2 - a**2*j**4 + b**2*c**2*i**2
               - b**2*i**2*j**2 - c**4*i**2 - c**2*i**4 + c**2*i**2*j**2)
'''
import math
from multiprocessing import Pool
import os


def positive_integer_roots(a, b, c):
    # Calculate the discriminant
    discriminant = b ** 2 - 4 * a * c

    # Check if discriminant is non-negative and a perfect square
    if discriminant < 0 or a == 0:
        return None
    sqrt_d = math.isqrt(discriminant)
    if sqrt_d ** 2 != discriminant:
        return None

    # Calculate the two potential roots
    root1 = (-b + sqrt_d) / (2 * a)
    root2 = (-b - sqrt_d) / (2 * a)

    # Collect positive integer roots
    positive_roots = [int(root) for root in (root1, root2) if root > 0 and root.is_integer()]

    # Return positive integer roots if any, otherwise None
    return positive_roots if positive_roots else None


def calculate_f_(args):
    a, b, c, i, j, goal = args
    r = (-a**4 + 2*a**2*b**2 + 2*a**2*c**2 + 4*a**2*i*j - 4*a**2*j**2 - b**4 + 2*b**2*c**2 - 4*b**2*i*j - c**4 - 4*c**2*i**2 + 4*c**2*i*j)
    s = (-2*a**4*j + 2*a**2*b**2*j + 2*a**2*c**2*i + 2*a**2*c**2*j + 2*a**2*i**2*j + 2*a**2*i*j**2 - 4*a**2*j**3 + 2*b**2*c**2*i - 2*b**2*i**2*j - 2*b**2*i*j**2 - 2*c**4*i - 4*c**2*i**3 + 2*c**2*i**2*j + 2*c**2*i*j**2)
    t = - a**4*j**2 - a**2*b**2*c**2 + a**2*b**2*j**2 + a**2*c**2*i**2 + a**2*c**2*j**2 + a**2*i**2*j**2 - a**2*j**4 + b**2*c**2*i**2 - b**2*i**2*j**2 - c**4*i**2 - c**2*i**4 + c**2*i**2*j**2
    fl = positive_integer_roots(r, s, t - goal)
    if fl:
        f = fl[0]
        print(f'goal = {goal}:', a, b, c, f+i, f+j, f)


if __name__ == '__main__':
    M = 200
    # goal = 144*3**2
    goal = 128
    # goal = 655
    with Pool(os.cpu_count()) as pool:
        for a in range(1, M+1):
            for b in range(1, a+1):
                for c in range(max(1, a-b), b+1):
                    tasks = []
                    for i in range(-a, a+1):
                        for j in range(-c, c+1):
                            tasks += [(a, b, c, i, j, goal)]
                    pool.map(calculate_f_, tasks)
