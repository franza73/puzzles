'''
a good word pair:
1. doesn't include a repetition of a letter right afterwards
2. containt exacty 12 letters
3. first word ends with same letter as second word begins

How many boxes are there? ---> very large number
three letters
C(26, 3) = N   ---> choose three distinct letters in 26
C(N, 4)        ---> choose four options for these triples

TODO:
1. From 'hash first second', come up with box.
2. Which hashes won't have a corresponding box?
'''
from collections import defaultdict
import re


W = []
B = defaultdict(list)
N = 16
with open('words_alpha.txt', 'r', encoding="ascii") as f:
    while True:
        line = f.readline()
        if not line:
            break
        word = line.strip()
        if not re.search(r'(\w)\1', word) and len(set(word)) <= N:
            W += [word]
            B[word[0]] += [word]

H = {}
for first in W:
    for second in B[first[-1]]:
        S = set(first).union(set(second))
        if len(S) > N:
            K = ''.join(sorted(S))
            if K not in H:
                H[K] = (str(len(K)), K, first, second)
            else:
                H[K] = None
for K in H:
    if H[K]:
        print(' '.join(H[K]))
