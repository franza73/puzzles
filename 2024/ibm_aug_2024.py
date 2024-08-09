'''
 1. Simulate the process, with avg and std_dev recursively
 2. multiprocess Pool --> use the max number of processors
 3. Compare the results of the two different methods
'''
from random import shuffle
from collections import Counter
import numpy as np


def calculate_p(total, sz, den=10**8):
    '''
    Estimates the Markov transition matrix
    '''
    n_bins = total // sz
    p = np.zeros([n_bins, n_bins])
    lin = 0
    for n in range(n_bins, 0, -1):
        lst = []
        for x in range(n):
            lst += [x]*sz
        cnt = Counter()
        for _ in range(den):
            shuffle(lst)
            v = 0
            for x in range(n):
                if len(set(lst[sz*x:sz*x+sz])) == 1:
                    v += 1
            cnt[v] += 1
        col = 0
        for i in sorted(cnt.keys()):
            p[lin, col+lin] = cnt[i]/den
            col += 1
        lin += 1
    return p


def avtime(q):
    '''
    Calculates the average time for the Markov Process
    '''
    x, y = q.shape
    # print('DEBUG:', x, y, q)
    v = np.linalg.inv(np.eye(x) - q) @ np.ones([x, 1])
    return v[0, 0]

# Q = np.array([[.5, .5, 0],
#               [0, .5, .5],
#               [.5, 0, 0]])

# P = np.array([[0.9913057, 0.0086099, 8.4e-05,   4e-07],
#               [0.0,       0.9822408, 0.0175885, 0.0001707],
#               [0.0,       0.0,       0.9714184, 0.0285816],
#               [0.0,       0.0,       0.0,       1]])

# for _ in range(1):
#     sz = 4
#     P = calculate_P(16, sz)
#     Q = P[0:(sz-2), 0:(sz-2)]
#     print(round(avtime(Q)))


def main():
    '''
    Resolves the puzzle
    '''
    for _ in range(16):
        sz = 5
        total = 50
        bins = total // sz
        p = calculate_p(total, sz)
        q = p[0:(bins-2), 0:(bins-2)]
        print(round(avtime(q)))


if __name__ == "__main__":
    main()
