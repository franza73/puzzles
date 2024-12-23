from math import log10
from functools import cache


@cache
def function(n):
    if n < 10:
        return 1
    k = int(log10(n)) + 1
    f, r = divmod(n, 10**(k-1))
    if f == 1:
        return function(10**(k-1)-1) + r + 1
    return (f-1)*function(10**(k-1)-1) + 10**(k-1)  + function(r)

n = 1456
#n = 1062880
n = 13947137600
#n = 99999999999999
# 728
print(function(n), n)