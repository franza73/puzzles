from math import sqrt

for ab in range(15, 155):
    for cd in range(15, 155):
        v = sqrt(ab**2 + cd**2)
        if int(v) * int(v) != int(v**2):
            continue
        for ad in range(15, 155):
            for bc in range(15, 155):
                w = sqrt(ad**2 + bc**2)
                if int(w) * int(w) != int(w**2):
                    continue
                if v == w and ab != ad and ab != bc and ab < cd and ad < bc:
                    print(ab,cd,ad,bc)



exit(0)
d = {}
for i in range(15, 155):
    for j in range(i+1, 155):
        v = i**2 + j**2
        sqrt_v = int(sqrt(v))
        if sqrt_v * sqrt_v == v:
            if v not in d:
                d[v] = [(i,j)]
            else:
                d[v] += [(i,j)]
            print(v, d[v])
exit(0)
for a in range(100, 12001):
    for b in range(a, 12001):
        ab = a + b
        sqrt_ab = int(sqrt(ab))
        if sqrt_ab * sqrt_ab == ab:
            print(ab)
