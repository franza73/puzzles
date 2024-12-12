from collections import Counter


cnt = Counter()
MAX = 999999999
best = {}
for i in range(1, MAX+1):
    for d in set(str(i)):
        if d == '0':
            continue
        cnt[d] += 1
        if cnt[d]*2 == i:
            best[d] = (cnt[d], i)
            print(d, cnt[d], i)
for d in sorted(best.keys()):
    print(d, best[d])

'''
for 1/2:
1 (531440, 1062880)
2 (1062881, 2125762)
3 (1594322, 3188644)
4 (2125763, 4251526)
5 (2657204, 5314408)
6 (3188645, 6377290)
7 (8503055, 17006110)
8 (9034496, 18068992)
9 (9565937, 19131874)

for 3/4
'''