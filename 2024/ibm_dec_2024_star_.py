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

# Make sure the function is correct for the example provided
n = 1456
assert function(1456) == 728

# Find the range where the solution should be found
for k in range(2, 15):
    n = 10**k - 1
    print(k, n, function(n)/ n)

# Apply binary search to find the larger solution
a, b = 10**13-1, 10**14-1
while a < b:
    m = (a + b) // 2
    if 4*function(m) < 3*m:
        a = m + 1 
    else:
        b = m - 1
assert 4*function(m) == 3*m
print(m)