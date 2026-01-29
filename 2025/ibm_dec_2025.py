'''
IBM Ponder this - December 2025

Here's my solution to the IBM Ponder This challenge for December 2025.

1. Problem description:
https://research.ibm.com/haifa/ponderthis/challenges/December2025.html

2. Comments about my solution:

Given the problem description, I calculated first all the primes that 
would be needed for the complete calculation.

For helping with this task, I used the Python module primesieve. 

The lists of primes were obtained, for
N = 10**8, in 1.24s, and for 
N = 10**9, in 13.1s.

So I started with the knowledge that the total calculation would not be 
dominated by prime number generation.

On this program, after the first step, the list p_low contains the first
 N primes >= 3, and the complete list p contains all the primes that need to be 
 considered for the final counting.

As i_1 points to the first prime that is > p_i + 2 * N, it needs to include 
numbers that can be larger than p[N-1] + 2 * N, and that's why I added an extra
 margin of 1000 for p_high calculation.

We can calculate the result by iterating (p_i) over all primes in p_low.
and counting how many primes in p are in the range [p_i + 2, p_i + 2 * N].

The trick is to perform this last count based on the indexes i_0 and i_1 of primes in p,
where i_0 is the index of the first prime >= p_i + 2, and i_1 is the index of the first
prime > p_i + 2 * N. As we progress through the increasing values of p_i, we also walk the
pointers i_0 and i_1 forward and then accumulate the difference (i_1 - i_0) to the result.

The pointer i_1 is initialized once before the main loop, as it only depends on N.

To illustrate the method, here is how the counting would work for N=5 and the first few primes:

i p_i  p_i+2  p_i+2N i_0 i_1 count p[i_0..i_1-1]
---------------------------------------------------------------
0  3     5      13    1   5    4   [5, 7, 11, 13]
1  5     7      15    2   5    3   [7, 11, 13]
2  7     9      17    3   6    3   [11, 13, 17]
3 11    13      21    4   7    3   [13, 17, 19]
4 13    15      23    5   8    3   [17, 19, 23]
Total count = 16, which matches the expected result f(5) = 16.

Results:
10**8   972989871151789 in 85.48s
10**9 87105187375692805 in 940.83s
'''
from primesieve import n_primes, primes, count_primes


# -- Generate primes --
N = 10**9
p_low = n_primes(N, 3)
p_high = primes(p_low[-1] + 2, p_low[-1] + 2 * N + 1000)
p = p_low + p_high
print(f'Step 1. Generated {len(p)} primes')

# -- Calculate initial indexes --
i_0 = 1
i_1 = count_primes(5, 3 + 2 * N)
print(f'Step 2. Calculated index i_1: {i_1}')

# -- Main loop and result --
res = 0
for pi in p_low:
    q_0 = pi + 2
    q_1 = pi + 2 * N
    while p[i_0] < q_0:
        i_0 += 1
    while p[i_1] <= q_1:
        i_1 += 1
    res += i_1 - i_0
print(f'Step 3. Calculated result: {res}')