# IBM Ponder This - January 2026

I solved the IBM Ponder This puzzle for January 2026: https://research.ibm.com/haifa/ponderthis/challenges/January2026.html, including the extra credits.

## First snippet
The following Python snippet implements the first idea that came to mind from reading the problem description:

```python
N = 10**6
valid_x = set()
for n in range(1, N + 1):
    for ai in A(n):
        x = n * ai
        if x in valid_x:
            continue
        if n in A(x):
            valid_x.add(x)
print(f'Result: {sum(valid_x)}')
```

It lists all the feasible `n`, and for each option of partition of `n`, defined in `A(n)`, obtains corresponding `x`, and tests the `(x, n)` pairs until all the valid `x` values are found. Sum them and return as the solution. 

I used the `valid_x` set, so that if `(x, n1)` and `(x, n2)` are valid pairs with `n1` different from `n2`, we do not count `x` twice, or try to evaluate again a value that we already know is valid.

My first implementation of the `A(n)` function is here:

```python
@cache
def A(n):
    if n == 0:
        return set([0])
    l = len(str(n))
    if n <= N:
        res = set([n])
    else:
        res = set()
    for k in range(1, l):
        a, b = divmod(n, 10**k)
        for c, d in product(A(a), A(b)):
            s = c + d
            if s <= N:
                res.add(s)
    return res
```

The first complete program used this same function for `i.` generating all partitions and for `ii.` searching a term among the partitions originated. 

For growing values of `N`, running it shows that we won't be able to scale up to $10^6$ in a reasonable amount of time.

The problem is that to check if `n` is in `A(x)`, we are generating all the partitions
for `x` and then checking if `n` in among these partitions. As `x` grows quite large, the implementation is inneficient even considering the attempts to trim everything larger than `N`.

We have at this point a complete solution to get started that is not effective for the sizes of `N` we care about.

## Second snippet

To address the `if n in A(x)` efficiency problem, we will for now keep `A()` as it is and write a better method to check `(x, n)` pair. The main part of the program will look like:

```python
N = 10**6
valid_x = set()
for n in range(1, N + 1):
    for ai in A(n):
        x = n * ai
        if x in valid_x:
            continue
        if can_sum_to(x, n):
            valid_x.add(x)
print(f'Result: {sum(valid_x)}')
```

And here's the new function:

```python
@cache
def can_sum_to(x, target):
    if x == target:
        return True
    if x < target:
        return False
    s = str(x)
    L = len(s)
    for k in range(1, L):
        a = int(s[:k])
        if a > target:
            break
        b = int(s[k:])
        if can_sum_to(b, target - a):
            return True
    return False
```

This now looks only into the ways to break the number `x` that can lead to adding to the target `n`.

At this point, we can expect improvement on the bottleneck and can get ready for larger values of `N`.

One step before that:

### Math insight

Before turning to a complete program, let's think about something that is constant for all the partitions of a number $n$: the digit sum taken $\mod 9$. 

Example: $A(123) = \{6, 15, 24, 123\}$, and all of these have digit sum congruent to $6 \mod 9$. 

Also remember that $a * b \mod 9  = a \mod 9 * b \mod 9$. 

Example: the terms of $123 \cdot A(123)$ all have module $n^2 = 36 = 0 \mod 9$.

So we can apply these ideas to `x` and obtain:

$x \mod 9 = n * ai \mod 9 = n \mod 9 * ai \mod 9 = n \mod 9 * n \mod 9$ and this is equal to $n \mod 9$ only if $n * (n - 1) = 0 \mod 9$, i.e. if $n$ is in $\{0, 1\} \mod 9$.

So we found a necessary condition on `n`.

## Third snippet

With the math insight, the main loop can now discard a large number of the original `n` values, as these don't lead to solutions for $x = n * ai$.

```python
def digit_sum_mod9(n):
    return sum(map(int, str(n))) % 9

N = 10**6
valid_x = set()
for n in range(1, N + 1):
    d_sum = digit_sum_mod9(n)
    if d_sum not in (0, 1):
        continue
    for ai in A(n):
        x = n * ai
        if x in valid_x:
            continue
        if can_sum_to(x, n):
            valid_x.add(x)
print(f'Result: {sum(valid_x)}')
```

It won't mean too much for efficiency, as the bottleneck was testing the `(x, n)` pairs, but I also improved the implementation of `A(n)`:

```python
@cache
def partition_sums(s):
    if not s:
        return {0}
    res = set()
    for k in range(1, len(s) + 1):
        head = int(s[:k])
        for t in partition_sums(s[k:]):
            res.add(head + t)
    return res

def A(n):
    return partition_sums(str(n))
```

The program could obtain the solution for $N = 10^6$ and crashed after over an hour for the $N = 10^7$ example.

I made modifications that allowed to run the calculation in batches and flush the `can_sum_to` cache after each batch and therefore decrease memory pressure and to get complete execution for the larger case.

## Results

The program produced the results:

    total elapsed 3.64 min for N = 10**6
    Result: 160808197419276

    total elapsed 105.90 min for N = 10**7
    Result: 26190672886645170

At this point, I had reached the goal for solving the problem and getting the extra credit.

I had added caching to `can_sum_to` almost naturally, and did not expect it to improve very much the calculations given the structure of its parameters. 

I was not ready for the next observation:

Removing caching for `can_sum_to` and rerunning the program, produced the same results, but in 1.57 min and 51.61 min respectively! There are so many calls to the `can_sum_to` function and what it 
does is so simple that the overhead of caching was very large, and with no associated gains to be observed.

## Conclusion

At this point, with the extra credit part solved in less than one hour, I did not have more pressure to
continue improving the time to obtain the solutions.