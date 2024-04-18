'''
Solves the IBM Poder This Puzzle for April 2024
'''
from itertools import product
from sympy.ntheory.modular import crt


def next_state(s: list, m: str) -> list:
    '''
    From current state and next move, find the next state.
    '''
    for i in range(3):
        if not s[i]:
            continue
        if s[i][-1] == 1:
            if m == '0':
                s[i].pop()
                s[(i+1) % 3].append(1)
                break
            if m == '1':
                s[i].pop()
                s[(i-1) % 3].append(1)
                break
        elif m == '2':
            if not s[(i-1) % 3] or s[(i-1) % 3][-1] > s[i][-1]:
                s[(i-1) % 3].append(s[i][-1])
                s[i].pop()
                break
            if not s[(i+1) % 3] or s[(i+1) % 3][-1] > s[i][-1]:
                s[(i+1) % 3].append(s[i][-1])
                s[i].pop()
                break
    return s


def find_parameters(n: int, move_seq: str) -> list:
    '''
    Simulates the process described in the problem and finds the parameters
    for the solution.
    '''
    state = [list(range(n, 0, -1)), [], []]
    stop = [[], list(range(n, 0, -1)), []]
    x = []
    i = 0
    k = 0
    x_sz = 50  # this is large enough for the conditions of this problem
    while k < x_sz:
        state = next_state(state, move_seq[i % len(move_seq)])
        i += 1
        if state == stop:
            x.append(i)
            k += 1
    lst0 = []
    for idx in range(1, len(x)):
        mod = x[idx] - x[0]
        if mod < x[0]:
            continue
        v = set(map(lambda xi, mod=mod: xi % mod, x))
        lst0.append((len(v), v, mod))
    best = min(lst0)
    assert x_sz / best[0] > 3
    return best[1:]


def test():
    '''
    Test the solution method with the parameters in the problem description.
    '''
    x0, mod_x = find_parameters(3, '0202112')
    y0, mod_y = find_parameters(4, '200211')
    lst = []
    for x0_i, y0_i in product(x0, y0):
        v = crt([mod_x, mod_y], [x0_i, y0_i])
        if v:
            lst += [v[0]]
    assert min(lst) == 932


def main():
    '''
    Solves the problem.
    '''
    moves = "12021121120020211202121"
    x0, mod_x = find_parameters(7, moves)
    moves = "0211202112002"
    y0, mod_y = find_parameters(10, moves)
    lst = []
    for x0_i, y0_i in product(x0, y0):
        v = crt([mod_x, mod_y], [x0_i, y0_i])
        if v:
            lst += [v[0]]
    print('Solution:', min(lst))

    moves = "202020200212121211212021202002020021211202021120211200200211" + \
            "20211211202002112021120211200212112020212120211"
    z0, mod_z = find_parameters(9, moves)
    lst = []
    for x0_i, y0_i, z0_i in product(x0, y0, z0):
        v = crt([mod_x, mod_y, mod_z], [x0_i, y0_i, z0_i])
        if v:
            lst += [v[0]]
    print('Solution star:', min(lst))

    # Solution: 16511310
    # Solution star: 1169723214


if __name__ == "__main__":
    main()
