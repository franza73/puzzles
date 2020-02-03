#l = [[3, 3, 2, 1], [3, 2, 3, 0], [3, 2, 3, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 0, 2, 3], [1, 1, 3, 3], [0, 2, 3, 3], [2, 3, 3, 2], [3, 2, 0, 3], [2, 2, 2, 3], [3, 3, 1, 2]]
l = [[3, 0, 3, 2], [3, 2, 3, 0], [3, 2, 0, 3], [3, 1, 1, 3], [0, 3, 3, 2], [2, 3, 1, 3], [3, 0, 2, 3], [3, 3, 3, 3], [1, 3, 3, 1], [1, 3, 2, 3], [3, 1, 3, 1], [2, 3, 3, 0]]
L = list('ABCDEFGHIJKL')

M = []
for i in range(3):
    M += [[]]
    for j in range(4):
        M[i] += ['']
#print(M)
for i, li in enumerate(l):
    for j, lii in enumerate(li):
        if lii < 3: 
            M[lii][j] += L[i]
#print(M)
s = '; '.join(['.'.join([M[i][j] for i in range(3)]) for j in range(4)])
print(s)
