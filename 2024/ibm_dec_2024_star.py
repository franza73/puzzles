from collections import Counter


cnt = Counter()
MAX = 99999999999
best = {}
d = '1'
cnt[d] = 10460353200 - 1
for i in range(13947137600, MAX+1):
    if d in str(i):
        cnt[d] += 1
        if cnt[d]*4 == i*3:
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
1 (10460353200, 13947137600)
'''